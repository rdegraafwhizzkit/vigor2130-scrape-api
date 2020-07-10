from device.vigor2130 import Vigor2130
from conf.config import config
from helper.global_helpers import dict_path_value as dpv

vigor_2130 = Vigor2130(
    url=dpv(config, 'vigor2130.url'),
    username=dpv(config, 'vigor2130.username'),
    password=dpv(config, 'vigor2130.password'),
    proxies=dpv(config, 'proxies')
)

print(vigor_2130.block_ip('1.2.3.4'))
