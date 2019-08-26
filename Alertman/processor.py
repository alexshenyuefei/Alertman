#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import datetime,time
from settings import EVENT_LOG_FILE, MAX_AGG_SECONDS, HOSTNAME
from sender.sendWeixin import sendweixin
from sender.sendWeixin2amend import sendweixin2amend
from sender.sendYunhu import yunhu
from alert2es import alert2es
from settings import ALERT_AMEND
#logger = EventLogger(EVENT_LOG_FILE)
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

Today = datetime.datetime.today()
Now = datetime.datetime.strftime(Today,'%Y-%m-%d-%H-%M-%S')
stoptime = datetime.datetime.strftime(Today,'%Y-%m-%d-08-30-00')
starttime =  datetime.datetime.strftime(Today, '%Y-%m-%d-23-00-00')

def zabbix_alert(data):
    if  data['type'] == 'zabbix':
          sendweixin(data['subject'].encode("utf-8"),data['message'].encode("utf-8"))
          try:
                alert2es(data['subject'].encode("utf-8"),data['message'].encode("utf-8"),data['type'])
		print "zabbix into es success!!"
          except:
		print "zabbix into failed!-^-"
                pass

    else:
          pass

def prometheus_alert(data):
    if data['type'] == 'prometheus':
        #params = {
        #    'timestamp': data['timestamp'],
        #    'subject': data['summary'],
        #    'message': data['description']
        #}
	#print data['summary']
	#print data['description']
        sendweixin(data['summary'],data['description'])
	try:
		alert2es(data['summary'],data['description'],data['type'])
		print "prometheus into es success!!"
	except:
		pass
    else:
	pass

def kibana_alert(data):
    if data['message']:
	try:
		if data['level']:
			if data['level'].encode("utf-8") == "高":
				print "高级别"
        			sendweixin(data['subject'].encode("utf-8"),data['message'].encode("utf-8"))
				try:
					if stoptime < Now < starttime:
					#	print "非发送时间点发送"
					#else:
						print "yunhu success",data['timestamp']
					#	yunhu(data['subject'].encode("utf-8"))
					else:
						print "夜间告警",data['timestamp']
				except:
					pass
			else:
				print "低级别:out",data['level'].encode("utf-8")
				#sendweixin2amend(data['subject'].encode("utf-8"),data['message'].encode("utf-8"))
	except:
		print "no level"
		sendweixin(data['subject'].encode("utf-8"),data['message'].encode("utf-8"))
                try:
			if stoptime < Now < starttime:
                        	print "no level yunhu success",data['timestamp']
			else:
				print "夜间告警",data['timestamp']
                        #yunhu(data['subject'].encode("utf-8"))
                except:
                        pass
    else:
	print "bottom"
	pass
