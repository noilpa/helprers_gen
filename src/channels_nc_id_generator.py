from sys import argv
from os.path import isdir, isfile
from xml.etree import ElementTree


def main():
    if len(argv) < 2:
        raise ValueError('data source path is not set')

    channel_ids = []
    for path in argv[1:]:
        if isfile(path):
            channel_ids.extend(parse_channel_id_from_xml(path))
        elif isdir(path):
            # get file list recursive parse all files in dir
            pass

    gen_helper(channel_ids)


def parse_channel_id_from_xml(path):
    et = ElementTree.parse(path)
    # TODO set right tag for parsing
    ids = []
    for el in et.iter('appointment'):
        ids.append((el.find('id').text, el.find('sdp_id').text))
    return ids


def gen_helper(ids):
    name = 'channels_id_gen.py'
    with open(name, 'w') as f:
        f.write('import http\n\n\n')
        f.write('def fill_pg_channels():\n')
        for i in range(len(ids)):
            f.write(
                f'\thttp.post_admin("/admin/channels", new_admin_channel(name="ch{i}", sdp_channel_id1={ids[i][1]}, '
                f'sdp_channel_id2={ids[i][0]}, number={i}))\n')


if __name__ == '__main__':
    main()
