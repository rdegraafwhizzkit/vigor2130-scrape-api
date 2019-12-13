from requests.auth import HTTPBasicAuth
import re
from conf.config import config
import grequests as gr


class Velop:
    def __init__(self, velops, username, password, proxies=None):
        self.velops = velops
        self.username = username
        self.password = password
        self.proxies = proxies if proxies is not None else {}

    def get_connected_clients(self):

        rs = [gr.get(
            f'http://{ip}/sysinfo.cgi',
            auth=HTTPBasicAuth(
                self.username,
                self.password
            ),
            proxies=self.proxies
        ) for name, ip in self.velops.items()]

        for r in gr.map(rs, size=3):
            try:
                request_ip = re.sub(r'^https?://([0-9a-z-.]+)/.*$', r'\1', r.url, re.I)
                name = [name for name, ip in self.velops.items() if ip == request_ip][0]

                section = False
                for line in r.content.decode('utf-8').split('\n'):
                    if line.startswith('Current connected client(s): ADDR'):
                        section = True
                    elif section and re.compile('[a-f0-9:]{17}', re.I).search(line) is not None:
                        yield {
                            'mac_address': re.sub(r'^.*([a-f0-9:]{17}).*$', r'\1', line),
                            'velop': name
                        }

                    if line.startswith('WMM mode'):
                        section = False
            except AttributeError:
                pass


if __name__ == "__main__":
    print([x for x in Velop(
        velops=config['velop']['velops'],
        username=config['velop']['username'],
        password=config['velop']['password'],
        proxies=config['proxies']
    ).get_connected_clients()])
