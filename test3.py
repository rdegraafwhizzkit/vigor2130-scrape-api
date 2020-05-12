from pprint import pprint as pp
from device.vigor2130 import Vigor2130
from conf.config import config
from helper.global_helpers import dict_path_value as dpv

proxies = dpv(config, 'proxies')

vigor_2130 = Vigor2130(
    url=dpv(config, 'vigor2130.url'),
    username=dpv(config, 'vigor2130.username'),
    password=dpv(config, 'vigor2130.password'),
    proxies=proxies
)

for line in vigor_2130.get_system_log():
    pp(line)
