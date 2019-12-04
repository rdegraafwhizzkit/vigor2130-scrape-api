import requests

class Vigor2130:
    def __init__(self, url, username, password, proxies=None):
        self.url = url
        self.username = username
        self.password = password
        self.proxies = proxies if proxies is not None else {}
        self.cookies = {}

    def login(self):
        r = requests.post(
            f'{self.url}/cgi-bin/webstax/login/login',
            data={'aa': self.username, 'ab': self.password},
            allow_redirects=False,
            proxies=self.proxies
        )

        self.cookies = {cookie.name: cookie.value for cookie in r.cookies if cookie.name == 'SESSION_ID_VIGOR'}

    def dhcp_table(self):
        r = requests.get(
            f'{self.url}/cgi-bin/webstax/stat/grocx_dhcp_status',
            cookies=self.cookies,
            allow_redirects=False,
            proxies=self.proxies
        )

        return [{'computer_name': z[0].lower(), 'ip_address': z[1], 'mac_address': z[2].lower(),
                 'expire_minutes': int(z[3])} for z in
                [y.split('/') for y in
                 [x for x in r.content.decode('utf-8').split('|') if x != '']]]

    def arp_cache(self):
        r = requests.get(
            f'{self.url}/cgi-bin/webstax/config/arp_table',
            cookies=self.cookies,
            allow_redirects=False,
            proxies=self.proxies
        )

        return [{'ip_address': z[0], 'mac_address': z[1].lower()} for z in
                [y.split('\t') for y in
                 [x for x in r.content.decode('utf-8').split('\n') if not x.startswith('IP Address')]]]

    def sessions_table(self):
        r = requests.get(
            f'{self.url}/cgi-bin/webstax/stat/session',
            cookies=self.cookies,
            allow_redirects=False,
            proxies=self.proxies
        )

        return [{
            'protocol': z[0].lower(),
            'src_ip': z[1].split(':')[0],
            'src_port': int(z[1].split(':')[1]),
            'dst_ip': z[2].split(':')[0],
            'dst_port': int(z[2].split(':')[1]),
            'state': z[3].lower() if len(z) == 4 else ''
        } for z in
            [y.split(' ') for y in
             [x for x in r.content.decode('utf-8').split('\n')]] if len(z) >= 3]

    def data_flow_monitor(self):
        r = requests.get(
            f'{self.url}/cgi-bin/webstax/config/dig_datam',
            cookies=self.cookies,
            allow_redirects=False,
            proxies=self.proxies
        )

        ss = r.content.decode('utf-8').split('|')

        data_flow_monitor_global = [{'ip_address': z[0], 'nr_sessions': int(z[1]), 'hardware_nat_rate_kbs': int(z[2])}
                                    for z in
                                    [y.split(',') for y in
                                     [x for x in ss[2].split(';') if x.strip() != '']]]

        data_flow_monitor_detailed = [{'ip_address': z[0], 'tx_rate_kbs': int(z[1]), 'rx_rate_kbs': int(z[2])} for z in
                                      [y.split(',') for y in
                                       [x for x in ss[3].split(';') if x.strip() != '']]]

        return {
            'global': data_flow_monitor_global,
            'detailed': data_flow_monitor_detailed
        }

    def ip_bind_mac(self):
        r = requests.get(
            f'{self.url}/cgi-bin/webstax/config/ipbmac',
            cookies=self.cookies,
            allow_redirects=False,
            proxies=self.proxies
        )

        return [{'ip_address': y[0], 'mac_address': y[1].lower(), 'computer_name': y[2].lower()} for y in
                [x.split(',') for x in
                 r.content.decode('utf-8').split('/')[2].split('|') if x.strip() != ''] if y[2].strip() != '']
