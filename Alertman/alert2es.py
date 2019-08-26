#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from elasticsearch import Elasticsearch

def alert2es(subject,message,source):
    	print "eseseseseses"
    	es = Elasticsearch( "172.21.120.30:9200" )
    	data = {
    	    "@timestamp":datetime.now().strftime( "%Y-%m-%dT%H:%M:%S.000+0800"),
    	    "subject":subject,
    	    "message":message,
    	    "source":source
    	} 
    	es.index( index="ops_alert", doc_type="alert", body=data )
    	#es.index( index="elastalert_status", doc_type="elastalert", body=data )



if __name__ == "__main__":
    alert2es(sys.argv[1],sys.argv[2],sys.argv[3])
