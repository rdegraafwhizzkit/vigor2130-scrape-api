from requests.auth import HTTPBasicAuth
import re
from conf.config import config
import grequests as gr


def get_velop_connected_clients():
    velops = config['velop']['velops']

    rs = [gr.get(
        f'http://{ip}/sysinfo.cgi',
        auth=HTTPBasicAuth(
            config['velop']['username'],
            config['velop']['password']
        )
    ) for name, ip in velops.items()]

    for r in gr.map(rs, size=3):
        try:
            request_ip = re.sub(r'^https?://([0-9a-z-.]+)/.*$', r'\1', r.url, re.I)
            name = [name for name, ip in velops.items() if ip == request_ip][0]

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
