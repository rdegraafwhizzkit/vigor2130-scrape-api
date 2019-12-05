import requests
from vigor2130_helpers import encode, LoginException, UnknownStatusException, NotLoggedInException


class Vigor2130:
    """The Vigor2130 object contains all functions to interact with the Vigor 2130 fiber modem

    Attributes:
        url (str): Base url to connect to the modem. E.g. http://192.168.1.254
        username (str): The encoded username
        password (str): The encoded password
        proxies (dict): Dictionary that holds the proxies to use, if any
        cookies (dict): Dictionary with necessary cookies to login to and interact with the modem

    """

    def __init__(self, url, username, password, proxies=None):
        """Init function for the Vigor2130 class

        Args:
            url (str): Base url to connect to the modem. E.g. http://192.168.1.254
            username (str): The username
            password (str): The password
            proxies (dict): A dictionary with proxies to use. Pass an empty dictionary {} or None for no proxies

        """
        self.url = url
        self.username = encode(username)
        self.password = encode(password)
        self.proxies = proxies if proxies is not None else {}
        self.cookies = {}
        self.logged_in = False

    def login(self):
        """Login function for the Vigor2130 modem

        Raises:
            LoginException: Raised if the login attempt was not successful

        """
        r = requests.post(
            f'{self.url}/cgi-bin/webstax/login/login',
            data={'aa': self.username, 'ab': self.password},
            allow_redirects=False,
            proxies=self.proxies
        )
        if r.headers['location'].startswith('/index.htm'):
            self.cookies = {cookie.name: cookie.value for cookie in r.cookies if cookie.name == 'SESSION_ID_VIGOR'}
            self.logged_in = True
        else:
            self.logged_in = False
            raise LoginException()

    def get(self, url, encoding='utf-8'):
        """Reusable get function to execute a requests get call and interpret the response

        Args:
            url (str): Relative url to get
            encoding (str): The encoding to use when interpreting the response body

        Returns:
            str: The content returned by the get request

        Raises:
            LoginException: Raised if the login attempt was not successful
            NotLoggedInException: Raised if the call was successful but the request got redirected to the login page
            UnknownStatusException: Raised if the call was not successful due to an unknown condition

        """

        if not self.logged_in:
            self.login()

        r = requests.get(
            f'{self.url}{url}',
            cookies=self.cookies,
            allow_redirects=False,
            proxies=self.proxies
        )

        if r.status_code == 200:
            return r.content.decode(encoding)

        if r.status_code == 302 and r.headers['location'].startswith('/login.htm'):
            raise NotLoggedInException()

        raise UnknownStatusException()

    def dhcp_table(self):

        content = self.get('/cgi-bin/webstax/stat/grocx_dhcp_status')

        return [{'computer_name': z[0].lower(), 'ip_address': z[1], 'mac_address': z[2].lower(),
                 'expire_minutes': int(z[3])} for z in
                [y.split('/') for y in
                 [x for x in content.split('|') if x != '']]]

    def arp_cache(self):

        content = self.get('/cgi-bin/webstax/config/arp_table')

        return [{'ip_address': z[0], 'mac_address': z[1].lower()} for z in
                [y.split('\t') for y in
                 [x for x in content.split('\n') if not x.startswith('IP Address')]]]

    def sessions_table(self):

        content = self.get('/cgi-bin/webstax/stat/session')

        return [{
            'protocol': z[0].lower(),
            'src_ip': z[1].split(':')[0],
            'src_port': int(z[1].split(':')[1]),
            'dst_ip': z[2].split(':')[0],
            'dst_port': int(z[2].split(':')[1]),
            'state': z[3].lower() if len(z) == 4 else ''
        } for z in
            [y.split(' ') for y in
             [x for x in content.split('\n')]] if len(z) >= 3]

    def data_flow_monitor(self):

        content = self.get('/cgi-bin/webstax/config/dig_datam')

        ss = content.split('|')

        data_flow_monitor_global = [
            {'ip_address': z[0], 'nr_sessions': int(z[1]), 'hardware_nat_rate_kbs': int(z[2])} for z in
            [y.split(',') for y in
             [x for x in ss[2].split(';') if x.strip() != '']]
        ]

        data_flow_monitor_detailed = [
            {'ip_address': z[0], 'tx_rate_kbs': int(z[1]), 'rx_rate_kbs': int(z[2])} for z in
            [y.split(',') for y in
             [x for x in ss[3].split(';') if x.strip() != '']]
        ]

        return {
            'global': data_flow_monitor_global,
            'detailed': data_flow_monitor_detailed
        }

    def ip_bind_mac(self):

        content = self.get('/cgi-bin/webstax/config/ipbmac')

        return [{'ip_address': y[0], 'mac_address': y[1].lower(), 'computer_name': y[2].lower()} for y in
                [x.split(',') for x in
                 content.split('/')[2].split('|') if x.strip() != ''] if y[2].strip() != '']
