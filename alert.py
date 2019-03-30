#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
from optparse import OptionParser
import tornado.web
import tornado.ioloop
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient
from tornado import httpclient
import urllib
from urllib import request
import json


logging.basicConfig(level=logging.INFO,format="%(asctime)s  - %(levelname)s - %(message)s")
logger=logging.getLogger(__name__)
WEB_HOOKS=dict()
DEFAULT_LISTEN_PORT=8060



def parse_opt():
    global WEB_HOOKS
    usage='''
    dingtalk alert for prometheus alertmanager .
    --port=8060
    --webhooks="group_1==dingtalk_webhook_url_1,group_2==dingtalk_webhook_url_2"

    Example:

     # send message to dingtalk_webhook_url_1
     curl -XPOST -H "Content-Type:application/json" -d"your_json_data"  localhost:8060/dingtalk/group_1/send

     # send message to dingtalk_webhook_url_2
     curl -XPOST -H "Content-Type:application/json" -d"your_json_data"  localhost:8060/dingtalk/group_2/send
    '''
    opt=OptionParser(usage)
    opt.add_option('-w','--webhooks',action='store',type='string')
    opt.add_option('-p','--port',action='store',type='string')
    options,args=opt.parse_args()
    urls=options.webhooks
    port=options.port
    if urls:
        for u in urls.split(','):
            k,v=u.split('==')
            if k and v:
                WEB_HOOKS[k]=v
    if port:
        try:
            DEFAULT_LISTEN_PORT=int(port)
            if DEFAULT_LISTEN_PORT <80  or DEFAULT_LISTEN_PORT > 65530:
                raise Exception("port range: 80 ~ 65530")
        except Exception as e:
            logger.info(str(e))
            logger.info("use default listen port 8060")
            DEFAULT_LISTEN_PORT=8060


class DingTalkHandler(tornado.web.RequestHandler):

    def initialize(self,webHook):
        self.webHook=webHook

    def prepare(self):
        if self.request.headers.get("Content-Type").startswith("application/json"):
            self.json_data=json.loads(self.request.body)
        else:
            self.json_data=None
    def post(self):
        mess='Prometheus Report: '+self.format_body()
        logger.info(mess)
        post_webhook(self.webHook,mess)


    def format_body(self):
        body=self.json_data
        print(body)
        status=body.get('status',' ')
        alerts=body.get('alerts',[])
        if alerts:
            info=alerts[0]
            annotations=info.get('annotations',' ')
            description=annotations.get('description',' ')
            summary=annotations.get('summary',' ')
            status=info.get('status',' ')
            startT=info.get('startsAt',' ')
            endT=info.get('endsAt',' ')
            labels=info.get('labels',{})
            if labels:
                label_mess=''
                for k,v in labels.items():
                    label_mess=label_mess+'\n'+k+":"+v
        mess= '''
Summary: %s
---------------------------
Description: %s
Status: %s
StartTime: %s
EndTime: %s
---------------------------
Labels: 
%s
         ''' %(summary,description,status,startT,endT,label_mess)
        return mess



def  post_webhook(url,mess):
    post_data={"msgtype":"text","text":{"content":mess}}
    headers={"Content-Type":"application/json"}
    try:
        json_data=bytes(json.dumps(post_data),'utf-8')
        r=request.Request(url=url,headers=headers,data=json_data)
        response=request.urlopen(r)
        logger.info(response.read())
    except Exception as e:
        logger.error(str(e))


async def async_webhook():
    url=""
    post_data={"msgtype":"text","text":{"content":"this is test message,"}}
    headers={"Content-Type":"application/json"}
    json_data=bytes(json.dumps(post_data),'utf-8')
    async_client=httpclient.AsyncHTTPClient()
    request=HTTPRequest(url=url,method="POST",headers=headers,body=json_data)
    try:
        response=await async_client.fetch(request)
    except Exception as e:
        logger.error(str(e))
    else:
        logger.info(response.body)




def start_app():
    routes=list()
    for alertName,alertUrl in WEB_HOOKS.items():
        routes.append(('/dingtalk/'+alertName+'/send',DingTalkHandler,dict(webHook=alertUrl)))
    application=tornado.web.Application(routes)
    print(DEFAULT_LISTEN_PORT)
    application.listen(DEFAULT_LISTEN_PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__=="__main__":
    parse_opt()
    start_app()
