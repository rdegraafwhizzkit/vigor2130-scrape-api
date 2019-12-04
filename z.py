from conf.config import config
from vigor2130 import Vigor2130
from pprint import pprint as pp

vigor_2130 = Vigor2130(
    url=config['url'],
    username=config['username'],
    password=config['password'],
    proxies=config['proxies']
)

pp(vigor_2130.dhcp_table())
pp(vigor_2130.arp_cache())
pp(vigor_2130.sessions_table())
pp(vigor_2130.ip_bind_mac())
pp(vigor_2130.data_flow_monitor())




