import requests
from requests.auth import HTTPBasicAuth
import re
from conf.config import config
import grequests as qqq

def get_velop_connected_clients():
    velops = config['velop']['velops']

    connected_clients = []
    for name, ip in velops.items():
        try:
            r = requests.get(
                f'http://{ip}/sysinfo.cgi',  # sysinfo_json.cgi also available
                auth=HTTPBasicAuth(
                    config['velop']['username'],
                    config['velop']['password']
                )
            )

            section = False
            for line in r.content.decode('utf-8').split('\n'):
                if line.startswith('Current connected client(s): ADDR'):
                    section = True
                elif section and re.compile('[a-f0-9:]{17}', re.I).search(line) is not None:
                    connected_clients.append(
                        {
                            'mac_address': re.sub(r'^.*([a-f0-9:]{17}).*$', r'\1', line),
                            'velop': name
                        }
                    )
                if line.startswith('WMM mode'):
                    section = False
        except Exception as ex:
            print(ex)

    return connected_clients


# urls = [
#     'http://192.168.1.236/sysinfo.cgi?name=living room',
#     'http://192.168.1.237/sysinfo.cgi?name=hallway',
#     'http://192.168.1.238/sysinfo.cgi?name=kitchen'
# ]
# from pprint import pprint as pp
# rs = [qqq.get(u, auth=HTTPBasicAuth(
#                     config['velop']['username'],
#                     config['velop']['password']
#                 )) for u in urls]
#
# for x in qqq.map(rs, size=3):
#     pp(x.request.url)
#     pp(x.content.decode('utf-8'))




