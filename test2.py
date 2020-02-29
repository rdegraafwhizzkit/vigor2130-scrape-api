import gevent.monkey

gevent.monkey.patch_all()

from device.vigor2130 import Vigor2130
from conf.config import config
from helper.global_helpers import dict_path_value as dpv
import pandas as pd
from pprint import pprint as pp
from chunker import get_velop_info
from target.es import index_objects

proxies = dpv(config, 'proxies')

vigor_2130 = Vigor2130(
    url=dpv(config, 'vigor2130.url'),
    username=dpv(config, 'vigor2130.username'),
    password=dpv(config, 'vigor2130.password'),
    proxies=proxies
)

vigor_info=vigor_2130.get_mac_ip_bind()
vigor_2130.logout()
# pp(vigor_info)

velop_info =[v for v in get_velop_info()]
# pp(velop_info)

df = pd.merge(
    pd.DataFrame(vigor_info),
    pd.DataFrame(velop_info),
    on="mac_address",
    how="inner"
).drop(
    columns=['ip_address', 'mac_address']
)

pp(df.to_dict(orient='records'))
if dpv(config, 'velop.index_data', False):
    try:
        index_objects(
            index=dpv(config, 'velop.index'),
            objects=df.to_dict(orient='records')
        )
    except Exception as ex:
        print(str(ex))
