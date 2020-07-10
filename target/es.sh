#!/bin/bash

ES_HOST=192.168.1.250

VIGOR2130=0
ICS2000=0
VELOP=0
OWM=0
SYSLOG=1

# Vigor 2130
if [ ${VIGOR2130} == 1 ]; then
  curl -XDELETE http://${ES_HOST}:9200/vigor2130
  curl -XPUT http://${ES_HOST}:9200/vigor2130
  curl -XPUT http://${ES_HOST}:9200/vigor2130/_mapping \
    -H "Content-Type: application/json" \
    --data-binary "@vigor2130-mapping.json"
fi

# ICS 2000
if [ ${ICS2000} == 1 ]; then
  curl -XDELETE http://${ES_HOST}:9200/ics2000
  curl -XPUT http://${ES_HOST}:9200/ics2000
  curl -XPUT http://${ES_HOST}:9200/ics2000/_mapping \
    -H "Content-Type: application/json" \
    --data-binary "@ics2000-mapping.json"
fi

# Velop
if [ ${VELOP} == 1 ]; then
  curl -XDELETE http://${ES_HOST}:9200/velop
  curl -XPUT http://${ES_HOST}:9200/velop
  curl -XPUT http://${ES_HOST}:9200/velop/_mapping \
    -H "Content-Type: application/json" \
    --data-binary "@velop-mapping.json"
fi

# OWM
if [ ${OWM} == 1 ]; then
  curl -XDELETE http://${ES_HOST}:9200/owm
  curl -XPUT http://${ES_HOST}:9200/owm
  curl -XPUT http://${ES_HOST}:9200/owm/_mapping \
    -H "Content-Type: application/json" \
    --data-binary "@owm-mapping.json"
fi

# SYSLOG
if [ ${SYSLOG} == 1 ]; then
  curl -XDELETE http://${ES_HOST}:9200/syslog
  curl -XPUT http://${ES_HOST}:9200/syslog
  curl -XPUT http://${ES_HOST}:9200/syslog/_mapping \
    -H "Content-Type: application/json" \
    --data-binary "@syslog-mapping.json"
fi
