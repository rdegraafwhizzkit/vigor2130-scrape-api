from vigor2130 import Vigor2130
from datetime import datetime
from conf.config import config
from vigor2130_helpers import get_info, NotLoggedInException
import time
import json
from elasticsearch import Elasticsearch
import hashlib
from requests.exceptions import ChunkedEncodingError

vigor_2130 = Vigor2130(
    url=config['url'],
    username=config['username'],
    password=config['password'],
    proxies=config['proxies']
)

es = Elasticsearch()

while True:

    seconds_since_epoch = int(time.time())
    this_hour = datetime.now().strftime("%Y%m%d%H")

    try:
        records = get_info(vigor_2130)
        with open(f'data/vigor2130-{this_hour}.json', 'a') as f:
            for record in records:
                record.update({'timestamp': seconds_since_epoch})
                record_json = json.dumps(record)
                f.write(record_json)
                f.write('\n')
                try:
                    res = es.index(
                        index="vigor2130",
                        doc_type='_doc',
                        body=record,
                        id=hashlib.sha224(record_json.encode('utf-8')).hexdigest()
                    )
                except:
                    print(f'Index error around {this_hour} for record {record_json}')
    except NotLoggedInException:
        print(f'NotLoggedInException around {this_hour}')
    except ChunkedEncodingError:
        print(f'ChunkedEncodingError around {this_hour}')

    time.sleep(25)
