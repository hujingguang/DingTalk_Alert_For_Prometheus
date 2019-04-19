#!/bin/bash - 
#===============================================================================
#
#          FILE: send.sh
# 
#         USAGE: ./send.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: hoover
#  ORGANIZATION: 
#       CREATED: 2019/03/30 09:43
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error




#!/bin/bash

alerts1='{
    "receiver": "admins",
    "status": "firing",
    "alerts": [
        {
            "status": "firing",
            "labels": {
                "alertname": "something_happend",
                "env": "prod",
                "instance": "server01.int:9100",
                "job": "node",
                "service": "prometheus_bot",
                "severity": "warning",
                "supervisor": "runit"
            },
            "annotations": {
                "summary": "Oops, something happend!"
            },
            "startsAt": "2016-04-27T20:46:37.903Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "https://example.com/graph#..."
        },
	 {
            "status": "firing",
            "labels": {
                "alertname": "good_happend",
                "env": "prod",
                "instance": "server02.int:9100",
                "job": "node",
                "service": "prometheus_bot",
                "severity": "warning",
                "supervisor": "runit"
            },
            "annotations": {
                "summary": "Oops, something happend!"
            },
            "startsAt": "2016-04-27T20:46:37.903Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "https://example.com/graph#..."
        }
    ],
    "groupLabels": {
        "alertname": "something_happend",
        "instance": "server01.int:9100"
    },
    "commonLabels": {
        "alertname": "something_happend",
        "env": "prod",
        "instance": "server01.int:9100",
        "job": "node",
        "service": "prometheus_bot",
        "severity": "warning",
        "supervisor": "runit"
    },
    "commonAnnotations": {
        "summary": "runit service prometheus_bot restarted, server01.int:9100"
    },
    "externalURL": "https://alert-manager.example.com",
    "version": "3"
}'

curl -XPOST -H "Content-Type:application/json" -d"$alerts1" http://127.0.0.1:8888/dingtalk/g1/send


