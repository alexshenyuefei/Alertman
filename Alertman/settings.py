#! /usr/bin/env python
# -*- coding: utf-8 -*-

HOSTNAME = '127.0.0.1'
# 记录报警事件的日志文件
EVENT_LOG_FILE = "./test.log"
# 记录用户信息的文件，用来支持按组发送功能
USER_INFO_FILE = "./user_info_sample.json"
# 聚合消息多久统一发送一次，单位是毫秒
AGG_LOOP_MS = 20000
## 告警的人员
ALERT_USER = ["amend1","amend2","amend2"]
#ALERT_USER = ["amend"]
ALERT_OPS = ["amend1","amend2","amend2"]
ALERT_DEV = ["amend1","amend2","amend2"]
ALERT_AMEND = ["amend"]
# 邮件服务器配置
MAIL_SERVER = "mail.xxxxxx.com"
MAIL_PORT = 25
MAIL_USER = "xxxxxx@iflytek.com"
MAIL_PWD = "xxxxxx"
MAIL_TO = "clge@xxxxxx.com"
# 云呼配置
YUNHU_URL = 'https://101.37.133.245:11008/'
YUNHU_ACCOUNTID = 'xxxxxxxxxxxxxxxxx'
YUNHU_TOKEN = 'xxxxxxxxxxxxxxxxx'
YUNHU_DISPLAY_NUMBER ='xxxxxxxxxxxxxxxxx'
# 动作文件配置目录
ACIONS_DIR = "./actions"
# 最长允许的聚合时间，单位是秒
MAX_AGG_SECONDS = 3600
# dingding 机器人回调地址
DINGDING_API_URL = ""
# 微信回调信息
CORPID='xxxxxxxxxxxxxxxxx'
APPSECRET='xxxxxxxxxxxxxxxxx'
AGENTID=1000002
TOUSER="gecailong"
