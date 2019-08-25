from os import walk
from os.path import isdir, isfile
from xml.etree import ElementTree
from json import loads
import re
from channels_nc_id_generator import ChannelNcIdTemplate

DEFAULT_CONFIG = 'config_gen.json'


class Generator:

    def __init__(self, template: object, cfg_path=DEFAULT_CONFIG):
        self.validate(template)
        self.name = to_snake(type(template).__name__)
        self.template = template
        self.cfg_path = cfg_path
        self.cfg = None

    def start(self):
        self._read_config()
        if self.cfg is None:
            raise ValueError

        files = self._get_file_list(self.cfg['input'])

        channel_ids = []
        for f in files:
            channel_ids.extend(self._parse_parent_tag(f))

        self.template.gen_helper(self.cfg['output'], channel_ids)

    def validate(self, template):
        if hasattr(template, 'parse_tags'):
            assert callable(template.parse_tags)
        else:
            raise ValueError
        if hasattr(template, 'gen_helper'):
            assert callable(template.gen_helper)
        else:
            raise ValueError

    def _read_config(self):
        with open(self.cfg_path, 'r') as f:
            cfg = loads(f.read())
        for item in cfg:
            if item['name'] == self.name:
                self.cfg = item
                break

    def _get_file_list(self, paths):
        files = []
        for path in paths:
            if isfile(path):
                files.append(path)
            elif isdir(path):
                files.extend(self._get_file_list(self._get_dir_tree(path)))
        return files

    def _get_dir_tree(self, path):
        depth = self.cfg['max_dir_depth']
        files = []
        # dirpath, dirnames, filenames
        for r, _, f in walk(path):
            if depth == 0:
                break
            # on windows join embeded dir with \\
            files += [r + '/' + file for file in f if file.endswith('.xml')]
            depth -= 1

        for i in range(len(files)):
            files[i] = files[i].replace('\\', '/')

        return files

    def _parse_parent_tag(self, path):
        et = ElementTree.parse(path)
        data = []
        for el in et.iter('appointment'):
            data.append(self.template.parse_tags(el))
        return data


def to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


if __name__ == '__main__':
    # Example
    c = ChannelNcIdTemplate()
    g = Generator(c)
    g.start()
