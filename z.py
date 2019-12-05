from conf.config import config
from vigor2130 import Vigor2130
from pprint import pprint as pp
import pandas as pd

vigor_2130 = Vigor2130(
    url=config['url'],
    username=config['username'],
    password=config['password'],
    proxies=config['proxies']
)

# pp(vigor_2130.dhcp_table())
# pp(vigor_2130.arp_cache())
# pp(vigor_2130.sessions_table())
# pp(vigor_2130.ip_bind_mac())
# pp(vigor_2130.data_flow_monitor())

df1 = pd.DataFrame(vigor_2130.dhcp_table())
df2 = pd.DataFrame([x for x in vigor_2130.ip_bind_mac() if x['computer_name'] != 'xklik aan klik uit basestation'])
df3 = pd.DataFrame(vigor_2130.data_flow_monitor()['detailed'])

df = pd.merge(
    df1,
    df2,
    on="mac_address",
    how="outer"
).drop(
    columns='ip_address_y'
).rename(
    columns={'ip_address_x': 'ip_address'}
)
df = pd.merge(
    df,
    df3,
    on='ip_address',
    how='outer'
)

df['computer_name'] = df.apply(
    lambda row: row.computer_name_x if pd.isna(row.computer_name_y) else row.computer_name_y, axis=1
)

df = df.drop(
    columns=['computer_name_x', 'computer_name_y']
)

pp(df.T.to_dict())
