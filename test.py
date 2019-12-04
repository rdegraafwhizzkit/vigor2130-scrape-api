from vigor2130 import Vigor2130
import time
from datetime import datetime
import json

from conf.config import config

vigor_2130 = Vigor2130(
    url=config['url'],
    username=config['username'],
    password=config['password'],
    proxies=config['proxies']
)

vigor_2130.login()

while True:

    seconds_since_epoch = int(time.time())

    device_info = {device['ip_address']: device for device in vigor_2130.dhcp_table()}
    for k, v in device_info.items():
        v.update(
            {
                'tx_rate_kbs': -1,
                'rx_rate_kbs': -1,
                'sessions': -1,
                'timestamp': seconds_since_epoch
            }
        )

    for k, v in {device['ip_address']: device for device in vigor_2130.data_flow_monitor()['detailed']}.items():
        if k in device_info:
            device_info[k].update(v)

    session_info = {}
    for j in [session['src_ip'] for session in vigor_2130.sessions_table() if
              session['src_ip'].startswith('192') and
              session['protocol'].lower() == 'tcp' and
              session['state'].lower() == 'established']:
        if j not in session_info:
            session_info[j] = {'ip_address': j, 'sessions': 1}
        else:
            session_info[j] = {'ip_address': j, 'sessions': session_info[j]['sessions'] + 1}

    for k, v in session_info.items():
        if k in device_info:
            device_info[k].update(v)

    for k, v in {device['ip_address']: device for device in vigor_2130.ip_bind_mac()}.items():
        if k in device_info:
            device_info[k].update(v)

    this_hour = datetime.now().strftime("%Y%m%d%H")
    with open(f'data/vigor2130-{this_hour}.json', 'a') as f:
        for device in [v for k, v in device_info.items()]:
            f.write(json.dumps(device))
            f.write('\n')

    time.sleep(1)

# select
#     computer_name
# ,   ip_address
# ,   mac_address
# ,   tx_rate_kbs
# ,   rx_rate_kbs
# ,   sessions
# ,   to_timestamp(`timestamp`) as `timestamp`
# from
#     dfs.scratch.vigor2130
# where
#     1=1
# and computer_name in ('huawei_p8_lite','my-iphone')--,'chromecast','raspberry pi')
# --or rx_rate_kbs >0 or tx_rate_kbs > 0
# order by
#     `timestamp` desc
# ,   computer_name
