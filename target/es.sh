#!/bin/bash

# Vigor 2130
#curl -XDELETE http://localhost:9200/vigor2130
#curl -XPUT http://localhost:9200/vigor2130
#curl -XPUT http://localhost:9200/vigor2130/_mapping \
#-H "Content-Type: application/json" \
#--data '{"properties":{"velop":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"computer_name":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"expire_minutes":{"type":"float"},"ip_address":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"mac_address":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"rx_rate_kbs":{"type":"float"},"timestamp":{"type":"date","format":"epoch_second"},"tx_rate_kbs":{"type":"float"}}}'

# ICS 2000
#curl -XDELETE http://localhost:9200/ics2000
#curl -XPUT http://localhost:9200/ics2000
#curl -XPUT http://localhost:9200/ics2000/_mapping \
#-H "Content-Type: application/json" \
#--data '{"properties":{"timestamp":{"type":"date","format":"yyyy-MM-dd HH:mm:ss"},"kWhHighReading":{"type":"double"},"kWhLowReading":{"type":"double"},"m3GassReading":{"type":"double"},"kWhHighUsage":{"type":"double"},"kWhLowUsage":{"type":"double"},"m3GassUsage":{"type":"double"},"kWhHighCost":{"type":"double"},"kWhLowCost":{"type":"double"},"m3GassCost":{"type":"double"}}}'

# Velop
#curl -XDELETE http://localhost:9200/velop
#curl -XPUT http://localhost:9200/velop
#curl -XPUT http://localhost:9200/velop/_mapping \
#-H "Content-Type: application/json" \
#--data '{"properties":{"velop":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"mac_address":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"timestamp":{"type":"date","format":"epoch_second"}}}'

# OWM
#curl -XDELETE http://localhost:9200/owm
#curl -XPUT http://localhost:9200/owm
#curl -XPUT http://localhost:9200/owm/_mapping \
#-H "Content-Type: application/json" \
#--data '{"properties":{"timestamp":{"type":"date","format":"epoch_second"},"sunrise":{"type":"date","format":"epoch_second"},"sunset":{"type":"date","format":"epoch_second"},"name":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"weather_main":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"weather_description":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"country":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}},"lon":{"type":"double"},"lat":{"type":"double"},"wind_speed":{"type":"double"},"temp":{"type":"double"},"feels_like":{"type":"double"},"temp_min":{"type":"double"},"temp_max":{"type":"double"},"visibility":{"type":"long"},"timezone":{"type":"long"},"pressure":{"type":"long"},"humidity":{"type":"long"},"wind_deg":{"type":"long"},"clouds_all":{"type":"long"}}}'


