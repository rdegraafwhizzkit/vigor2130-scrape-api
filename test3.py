from pprint import pprint as pp
from device.vigor2130 import Vigor2130
from conf.config import config
from helper.global_helpers import dict_path_value as dpv
from target.es import index_objects
import time

vigor_2130 = Vigor2130(
    url=dpv(config, 'vigor2130.url'),
    username=dpv(config, 'vigor2130.username'),
    password=dpv(config, 'vigor2130.password'),
    proxies=dpv(config, 'proxies')
)

while True:

    try:
        if dpv(config, 'syslog.index_data', False):
            objects = index_objects(
                index=dpv(config, 'syslog.index'),
                objects=[o for o in vigor_2130.get_system_log()]
            )
            print(f'Indexed {objects} objects')
    except Exception as ex:
        print(str(ex))

    time.sleep(int(dpv(config, 'syslog.sleep', 300)))
