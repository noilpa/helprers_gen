class ChannelNcIdTemplate:

    def parse_tags(self, element):
        return element.find('id').text, element.find('sdp_id').text

    def gen_helper(self, output: str, data: list):
        with open(output, 'w') as f:
            f.write('import http\n\n\n')
            f.write('def fill_pg_channels():\n')
            for i in range(len(data)):
                f.write(
                    f'\thttp.post_admin("/admin/channels", new_admin_channel(name="ch{i}", '
                    f'sdp_channel_id1={data[i][1]}, sdp_channel_id2={data[i][0]}, number={i}))\n')
