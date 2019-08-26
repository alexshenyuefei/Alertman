#!/bin/python
#-*- coding: utf-8 -*-

import requests
import sys
import os
import json
import logging
import time

time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

logging.basicConfig(level = logging.INFO, format = '%(asctime)s, %(filename)s, %(levelname)s, %(message)s',
                datefmt = '%a, %d %b %Y %H:%M:%S',
                filename = os.path.join('/tmp','weixin.log'),
                filemode = 'a')
def sendweixin(data):
    # 微信接口参数
    # 根据自己申请的企业微信上接口参数调整；
    corpid='xxxxxxxxxxxxxxxx'
    appsecret='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    agentid=1000002
    
    #获取accesstoken
    token_url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret
    req=requests.get(token_url)
    accesstoken=req.json()['access_token']
    #发送消息
    msgsend_url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken
    print msgsend_url
    print type(data)
   
    params = {
      "touser" : "gecailong",
      "msgtype" : "text",
      "agentid" : agentid,
      "text" : {
	"content":data['message']
	},
}	
 
    req=requests.post(msgsend_url, data=json.dumps(params))
    
    # 写日志
    #logging.info('sendto:' + touser + ';;subject:' + subject + ';;message:' + message)
if __name__=="__main__":
    sendweixin(sys.argv[1])
