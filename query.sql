select
    computer_name
,   ip_address
,   mac_address
,   tx_rate_kbs
,   rx_rate_kbs
,   sessions
,   to_timestamp(`timestamp`) as `timestamp`
,   expire_minutes
from
    dfs.vigor2130.data
where
    1=1
and (rx_rate_kbs >0 or tx_rate_kbs > 0)
order by
    `timestamp` desc
,   computer_name