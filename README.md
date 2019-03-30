# DingTalk_For_Prometheus
钉钉告警For Prometheus AlertManager


Usage:
  ./alert.py  --help


Docker

   docker pull hooversa/dingtalk_alert

   docker run --name alert -p 8888:8888 -d hooversa/dingtalk_alert ./alert.py -p 8888 -w g1==your_dingtalk_webhook


