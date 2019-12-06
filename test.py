from vigor2130 import Vigor2130
from datetime import datetime
from conf.config import config
from vigor2130_helpers import get_info
import time
import json

vigor_2130 = Vigor2130(
    url=config['url'],
    username=config['username'],
    password=config['password'],
    proxies=config['proxies']
)

while True:

    seconds_since_epoch = int(time.time())
    this_hour = datetime.now().strftime("%Y%m%d%H")

    with open(f'data/vigor2130-{this_hour}.json', 'a') as f:
        for record in get_info(vigor_2130):
            record.update({'timestamp': seconds_since_epoch})
            f.write(json.dumps(record))
            f.write('\n')

    time.sleep(25)
