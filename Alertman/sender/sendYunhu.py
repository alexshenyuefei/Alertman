#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import hashlib
import base64
import requests
import json
import ssl
import sys
import urllib3
urllib3.disable_warnings()

from settings import YUNHU_URL, YUNHU_ACCOUNTID, YUNHU_TOKEN, YUNHU_DISPLAY_NUMBER
#YUNHU_URL = 'https://101.37.133.245:11008/'
#YUNHU_ACCOUNTID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
#YUNHU_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxx'
#YUNHU_DISPLAY_NUMBER ='xxxxxxxxxxxxxxxxxxx'

def yunhu(content):
    ssl._create_default_https_context = ssl._create_unverified_context
    platform = 'voice'
    version = 'v1.0.0'
    functionCode = 'notify'
    accountId = YUNHU_ACCOUNTID
    token = YUNHU_TOKEN

    t = str(int(round(time.time() * 1000)))

    payload_str = accountId+token+t
    hl = hashlib.md5()
    #hl.update(payload_str.encode(encoding='utf-8'))
    try:
        hl.update(payload_str)
    except TypeError:
        hl.update(payload_str.encode(encoding='utf-8'))
    sig = hl.hexdigest()
    try:
        authorization = base64.b64encode(accountId+':'+t)
    except TypeError:
        authorization = base64.b64encode((accountId+':'+t).encode())
    url = YUNHU_URL+platform+'/'+version+'/'+functionCode+'/'+accountId+'/'+sig

    data = json.dumps({
    "verifyCode":"1234",
    "displayNumber":YUNHU_DISPLAY_NUMBER,
    "calleeNumber":"17621421476",
    "replayTimes":"3",
    "callbackUrl":"",
    "templateID":"400605",
    "templateArgs":{"test":content},
    "callbackUrl":"http://132.232.1.236:8000/"
    })
    header_dict = {"Host": "101.37.133.245:11008","Authorization": authorization,"Accept": "application/json","Content-Type": "application/json"}

    try:
        return requests.get(url, headers=header_dict, data=data, verify=False, timeout=5).text
    except:
	print error
        return False

if __name__=="__main__":
    yunhu(sys.argv[1])
