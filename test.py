from device.vigor2130 import Vigor2130
from device.velop import Velop
from device.ics2000 import ICS2000
from conf.config import config
from helper.vigor2130_helpers import get_info, NotLoggedInException
from datetime import datetime
import time
from requests.exceptions import ChunkedEncodingError
from target.es import index_objects

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

if False:
    ics2000_info = [o for o in ICS2000(
        mac_address=config['ics2000']['mac_address'],
        email_address=config['ics2000']['email_address'],
        password=config['ics2000']['password'],
        proxies=config['proxies']
    ).get_info()]

    index_objects(
        index=config['ics2000']['index'],
        objects=ics2000_info
    )

    print(ics2000_info)

index_objects(
    index=config['velop']['index'],
    objects=[client for client in velop.get_connected_clients()]
)

exit(1)

while True:

    this_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        velop_info = [client for client in velop.get_connected_clients()]
        records = get_info(vigor_2130, velop_info)

        if config['vigor2130']['index_data']:
            index_objects(
                index=config['vigor2130']['index'],
                objects=records
            )
        vigor_2130.logout()
    except NotLoggedInException:
        print(f'NotLoggedInException at {this_time}')
    except ChunkedEncodingError:
        print(f'ChunkedEncodingError at {this_time}')
    except Exception as ex:
        print(ex)

    time.sleep(600)
