import requests
from requests.auth import HTTPBasicAuth
import re
import time
from conf.config import config
from helper.global_helpers import dict_path_value as dpv


def get_velop_info():

    timestamp = int(time.time())

    for name, ip in dpv(config,'velop.velops').items():

        response = requests.get(
            url=f'http://{ip}/sysinfo.cgi',
            auth=HTTPBasicAuth(
                dpv(config,'velop.username'),
                dpv(config,'velop.password')
            ),
            stream=True
        )

        body = ''
        for content in response.iter_content(16384):
            body = body + content.decode('utf-8')
            if 'Wi-Fi syscfg section' in body:
                break

        section = False
        for line in body.split('\n'):
            if line.startswith('Current connected client(s): ADDR'):
                section = True
            elif section and re.compile('[a-f0-9:]{17}', re.I).search(line) is not None:
                yield {
                    'mac_address': re.sub(r'^.*([a-f0-9:]{17}).*$', r'\1', line).lower(),
                    'velop': name,
                    'timestamp': timestamp
                }

            if line.startswith('WMM mode'):
                section = False
