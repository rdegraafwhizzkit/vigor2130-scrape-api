from device.owm import OWM
from helper.global_helpers import dict_path_value as dpv
from conf.config import config
from target.es import index_objects, sha224
from time import sleep, time


proxies = dpv(config, 'proxies')

owm = OWM(
    url=dpv(config, 'owm.url'),
    id=dpv(config, 'owm.id'),
    app_id=dpv(config, 'owm.appid'),
    units=dpv(config, 'owm.units'),
    proxies=proxies
)

# OWM
if dpv(config, 'owm.index_data', False):
    while True:
        try:
            index_objects(
                index=dpv(config, 'owm.index'),
                objects=owm.get_info(),
                id_function=lambda x: sha224(3600*int(int(x['timestamp'])/3600))
            )
        except Exception as ex:
            print(str(ex))

        sleep(3000)