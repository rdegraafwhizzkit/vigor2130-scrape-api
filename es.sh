#!/bin/bash

curl -XDELETE http://localhost:9200/vigor2130
curl -XPUT http://localhost:9200/vigor2130

curl -XPUT http://localhost:9200/vigor2130/_mapping \
-H "Content-Type: application/json" \
--data '{"properties":{"velop":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"computer_name":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"expire_minutes":{"type":"float"},"ip_address":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"mac_address":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"rx_rate_kbs":{"type":"float"},"timestamp":{"type":"date","format":"epoch_second"},"tx_rate_kbs":{"type":"float"}}}'
