#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import sys
import os

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass


HEADERS = {'Content-Type': 'application/json;charset=utf-8'}


class  senddingding(object):
        def __init__(self, API_URL, CONTENT):
            self.api_url = API_URL
            self.headers = HEADERS
            self.content = CONTENT

#        def action(self)
#            if self.source == 'promethues':
#                alert_data = json.dumps(content).encode("utf-8")
#                    annotations = {}
#                    for k, v in alert_data['annotations'].items():
#                        try:
#                            annotations[k] = v.format(**labels)
#                        except Exception:
#                            annotations[k] = v
#                    print annotations
#            else if self.source == 'zabbix':
#                pass
#            else if self.source == 'aliyun':
#                pass
#            else
#                pass

        def msg(self):
            json_text= {
                "msgtype": "text",
                "text": {
                    "content": self.content
                }
            }
            requests.post(self.api_url,json.dumps(json_text),headers=self.headers)

if __name__ == '__main__':
    API_URL = "https://oapi.dingtalk.com/robot/send?access_token=0be34beea3014e2124d7dbfe13746819c8c95799eb66f91dbe1c969c80ed7510"
    obj = senddingding(API_URL,sys.argv[1])
    obj.msg()
