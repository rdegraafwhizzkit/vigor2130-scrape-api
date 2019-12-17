import gevent.monkey

gevent.monkey.patch_all()

from device.vigor2130 import Vigor2130
from device.velop import Velop
from device.ics2000 import ICS2000
from device.owm import OWM
from conf.config import config
from helper.vigor2130_helpers import NotLoggedInException
from helper.global_helpers import get_joined_data
from datetime import datetime
from requests.exceptions import ChunkedEncodingError
from target.es import index_objects, sha224

vigor_2130 = Vigor2130(
    url=config['vigor2130']['url'],
    username=config['vigor2130']['username'],
    password=config['vigor2130']['password'],
    proxies=config['proxies']
)

velop = Velop(
    velops=config['velop']['velops'],
    username=config['velop']['username'],
    password=config['velop']['password'],
    proxies=config['proxies']
)

ics2000 = ICS2000(
    mac_address=config['ics2000']['mac_address'],
    email_address=config['ics2000']['email_address'],
    password=config['ics2000']['password'],
    proxies=config['proxies']
)

owm = OWM(
    url=config['owm']['url'],
    id=config['owm']['id'],
    app_id=config['owm']['appid'],
    units=config['owm']['units']

)

# OWM
print('OWM')
if config['owm']['index_data']:
    try:
        index_objects(
            index=config['owm']['index'],
            objects=owm.get_info(),
            id_function=lambda x: sha224(x['timestamp'])
        )
    except Exception as ex:
        print(str(ex))

# ICS2000
print('ICS2000')
if config['ics2000']['index_data']:
    try:
        index_objects(
            index=config['ics2000']['index'],
            objects=[o for o in ICS2000(
                mac_address=config['ics2000']['mac_address'],
                email_address=config['ics2000']['email_address'],
                password=config['ics2000']['password'],
                proxies=config['proxies']
            ).get_info()],
            id_function=lambda x: sha224(x['timestamp'])
        )
    except Exception as ex:
        print(str(ex))

# Vigor2130
print('Vigor2130')
this_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    velop_info = [client for client in velop.get_info()]

    if config['vigor2130']['index_data']:
        index_objects(
            index=config['vigor2130']['index'],
            objects=get_joined_data(vigor_2130, velop_info)
        )
    vigor_2130.logout()

    # Velop
    print('Velop')
    if config['velop']['index_data']:
        try:
            index_objects(
                index=config['velop']['index'],
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
