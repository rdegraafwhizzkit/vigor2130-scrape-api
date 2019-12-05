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

df1 = pd.DataFrame(vigor_2130.dhcp_table()).set_index('mac_address', drop=False)
df2 = pd.DataFrame(vigor_2130.ip_bind_mac()).set_index('mac_address', drop=True)
df3 = pd.DataFrame(vigor_2130.data_flow_monitor()['detailed']).set_index('ip_address', drop=True)

pp(df3)

df = df1.merge(df2, left_index=True, right_index=True, how="outer")
# df.set_index()
df4 = df.merge(df3, left_index=True, right_index=True, how="outer")

# pp(df)
# pp(df.T.to_dict())

# pp(df4)
pp(df4.T.to_dict())