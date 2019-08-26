#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import web, ioloop
import time
import json
import os,sys
import argparse
import ast
from datetime import datetime
from elasticsearch import Elasticsearch
from processor import zabbix_alert,prometheus_alert,kibana_alert
from settings import ACIONS_DIR, MAX_AGG_SECONDS, AGG_LOOP_MS

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


class AlertHandler(web.RequestHandler):
    def post(self):
        try:
	    payload = json.loads(self.request.body)
        except json.decoder.JSONDecodeError:
            raise web.HTTPError(400)
        time = payload['timestamp']
        subject = payload['subject']
        message = payload['message']
        data = {
               'type':'zabbix',
               'timestamp':time,
               'subject':subject,
               'message':message
               }
        return zabbix_alert(data)

class ZabbixCallbackHandler(web.RequestHandler):
    def post(self):
        try:
           # payload = json.loads(self.request.body)
	    payload = dict(self.request.body)
        except json.decoder.JSONDecodeError:
            raise web.HTTPError(400)
        actions = payload.get("actions")
        data = payload.get("data")
        if actions and data:
            actions_file = os.path.join(ACIONS_DIR, "{}.json".format(actions))
            if not os.path.exists(actions_file):
                raise web.HTTPError(400)
            with open(actions_file, "r") as f:
                actions = json.loads(f.read())
            #self.write({"result": do_actions(actions["actions"], data)})
        else:
            raise web.HTTPError(400)

class PrometheusCallbackHandler(web.RequestHandler):

    def post(self):
        try:
            payload = eval(self.request.body)
	    print payload
        except json.decoder.JSONDecodeError:
            raise web.HTTPError(400)
        level = payload['commonLabels']['level']
        alertname = payload['commonLabels']['alertname']
        service = payload['commonLabels']['service']
        alert_row = payload['alerts']
        description = ""
        summary = ""
        try:
            description =  alert_row[0]['annotations']['description']
            summary =  alert_row[0]['annotations']['summary']
        except:
            pass
	if payload['status'] != "resolved":
        	data = {
        	    'type':"prometheus",
        	    '@timestamp': datetime.now().strftime( "%Y-%m-%dT%H:%M:%S.000+0800" ),
        	    'level': level,
        	    'alertname': alertname,
        	    'description': description,
        	    'summary': summary,
        	    'service': service,
        	    'status': payload['status']
        	}
		prometheus_alert(data)
	else:
		pass

class KibanaCallbackHandler(web.RequestHandler):

    def post(self):
        try:
            payload = json.loads(self.request.body)
        except json.decoder.JSONDecodeError:
            raise web.HTTPError(400)
	print "kibana:",payload
        message = payload['message']
        subject = payload['subject']
	try:
	    percentage = payload['percentage']
	    if percentage > '50':
	         level = payload['_err_level']
	         c_count = payload['not_match_count']
	         h_hits = payload['num_hits']
	         message_v = message +",级别:"+level+" ,可用率:"+str(percentage)+ ", 异常数:"+str(c_count) +" ,总计"+str(h_hits)
                 data = {
                      'type':'kibana',
                      'timestamp': int(time.time()),
                      'message': message_v,
	              'level':level,
                      'subject': subject
                 }
	    else:
                level = payload['_err_level']
                c_count = payload['not_match_count']
                h_hits = payload['num_hits']
	        message_v = message +",级别:"+ level +" ,错误率:"+str(percentage)+ "% ,正常数:"+str(c_count) +" ,总计"+str(h_hits)
                data = {
                     'type':'kibana',
                     'timestamp': int(time.time()),
                     'message': message_v,
                     'level':level,
                     'subject': subject
                }
	except:
            data = {
                'type':'kibana',
                'timestamp': int(time.time()),
                'message': message,
                'subject': subject
            }
	print data
        return kibana_alert(data)

def make_app():
    return web.Application([
        (r"/alert", AlertHandler),
        (r"/alert/prometheus", PrometheusCallbackHandler),
	(r"/alert/zabbix", ZabbixCallbackHandler),
	(r"/alert/kibana", KibanaCallbackHandler)
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='监听端口', default=8088)
    parser.add_argument('--host', type=str, help='监听地址', default="0.0.0.0")
    args = parser.parse_args()
    app = make_app()
    app.listen(port=args.port, address=args.host)
    print ("start app on 8088")
    ioloop.IOLoop.current().start()
