import gevent.monkey

gevent.monkey.patch_all()

from device.vigor2130 import Vigor2130
from device.velop import Velop
from device.ics2000 import ICS2000
from device.owm import OWM
from conf.config import config
from helper.vigor2130_helpers import NotLoggedInException
from helper.global_helpers import get_joined_data, dict_path_value as dpv
from datetime import datetime
from requests.exceptions import ChunkedEncodingError
from target.es import index_objects, sha224

proxies = dpv(config, 'proxies')

vigor_2130 = Vigor2130(
    url=dpv(config, 'vigor2130.url'),
    username=dpv(config, 'vigor2130.username'),
    password=dpv(config, 'vigor2130.password'),
    proxies=proxies
)

velop = Velop(
    velops=dpv(config, 'velop.velops'),
    username=dpv(config, 'velop.username'),
    password=dpv(config, 'velop.password'),
    proxies=proxies
)

ics2000 = ICS2000(
    mac_address=dpv(config, 'ics2000.mac_address'),
    email_address=dpv(config, 'ics2000.email_address'),
    password=dpv(config, 'ics2000.password'),
    proxies=proxies
)

owm = OWM(
    url=dpv(config, 'owm.url'),
    id=dpv(config, 'owm.id'),
    app_id=dpv(config, 'owm.appid'),
    units=dpv(config, 'owm.units'),
    proxies=proxies
)

# OWM
print('OWM')
if dpv(config, 'owm.index_data', False):
    try:
        index_objects(
            index=dpv(config, 'owm.index'),
            objects=owm.get_info(),
            id_function=lambda x: sha224(x['timestamp'])
        )
    except Exception as ex:
        print(str(ex))

# ICS2000
print('ICS2000')
if dpv(config, 'ics2000.index_data', False):
    try:
        index_objects(
            index=dpv(config, 'ics2000.index'),
            objects=[o for o in ics2000.get_info()],
            id_function=lambda x: sha224(x['timestamp'])
        )
    except Exception as ex:
        print(str(ex))

# Vigor2130
print('Vigor2130')
this_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    velop_info = [client for client in velop.get_info()]

    if dpv(config, 'vigor2130.index_data', False):
        index_objects(
            index=dpv(config, 'vigor2130.index'),
            objects=get_joined_data(vigor_2130, velop_info)
        )
    vigor_2130.logout()

    # Velop
    print('Velop')
    if dpv(config, 'velop.index_data', False):
        try:
            index_objects(
                index=dpv(config, 'velop.index'),
                objects=velop_info
            )
        except Exception as ex:
            print(str(ex))

except NotLoggedInException:
    print(f'NotLoggedInException at {this_time}')
except ChunkedEncodingError:
    print(f'ChunkedEncodingError at {this_time}')
except Exception as ex:
    print(str(ex))

print('Done')
