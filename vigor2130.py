import requests


class Vigor2130:

    def __init__(self, url, username, password, proxies=None):
        '''
        The Vigor2130 object contains all functions to interact with the Vigor 2130 fiber modem

        Args:
            url (str): Base url to connect to the modem. E.g. http://192.168.1.254
            username (str): The username
            password (str): The password
            proxies (dict): A dictionary with proxies to use, if needed. Pass an empty dictionary {} or None for no proxies

        Attributes:
            url (str): Base url to connect to the modem. E.g. http://192.168.1.254
            username (str): The encoded username
            password (str): The encoded password
            proxies (dict): Dictionary that holds the proxies to use, if any
            cookies (dict): Dictionary with necessary cookies to login to and interact with the modem
        '''

        self.url = url
        self.username = self.encode(username)
        self.password = self.encode(password)
        self.proxies = proxies if proxies is not None else {}
        self.cookies = {}

    def encode(self, input_string):
        lookup_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        output_string = ""

        i = 0

        while True:
            chr1 = ord(input_string[i]) if i < len(input_string) else None
            i = i + 1

            chr2 = ord(input_string[i]) if i < len(input_string) else None
            i = i + 1

            chr3 = ord(input_string[i]) if i < len(input_string) else None
            i = i + 1

            enc1 = chr1 >> 2 if chr1 is not None else 0
            enc2 = (((chr1 if chr1 is not None else 0) & 3) << 4) | (chr2 >> 4 if chr2 is not None else 0)
            if chr2 is None:
                enc3 = enc4 = 64
            elif chr3 is None:
                enc3 = ((chr2 & 15) << 2)
                enc4 = 64
            else:
                enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
                enc4 = chr3 & 63

            output_string = output_string + lookup_table[enc1] + lookup_table[enc2] + lookup_table[enc3] + lookup_table[
                enc4]

            if i >= len(input_string):
                break

        return output_string

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
