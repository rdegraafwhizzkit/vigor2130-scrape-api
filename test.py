from vigor2130 import Vigor2130
from datetime import datetime
from conf.config import config
from vigor2130_helpers import get_info, NotLoggedInException
import time
import json
from elasticsearch import Elasticsearch
import hashlib
from requests.exceptions import ChunkedEncodingError
import velop


vigor_2130 = Vigor2130(
    url=config['url'],
    username=config['username'],
    password=config['password'],
    proxies=config['proxies']
)

es = Elasticsearch(hosts=config['es']['hosts'])

while True:

    this_hour = datetime.now().strftime("%Y%m%d-%H")
    this_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        velop_info = velop.get_velop_connected_clients()
        records = get_info(vigor_2130, velop_info)

        with open(f'data/vigor2130-{this_hour}.json', 'a') as f:
            for record in records:
                record.update({'timestamp': int(time.time())})
                record_json = json.dumps(record)
                f.write(record_json)
                f.write('\n')
                if config['es']['index_data']:
                    try:
                        res = es.index(
                            index=config['es']['index'],
                            doc_type=config['es']['doc_type'],
                            body=record,
                            id=hashlib.sha224(record_json.encode('utf-8')).hexdigest()
                        )
                    except:
                        print(f'Index error at {this_time} for record {record_json}')
        vigor_2130.logout()
    except NotLoggedInException:
        print(f'NotLoggedInException at {this_time}')
    except ChunkedEncodingError:
        print(f'ChunkedEncodingError at {this_time}')
    except Exception as ex:
        print(ex)

    time.sleep(300)
