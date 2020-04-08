#!/usr/bin/env python

from datetime import datetime
import certifi
import configparser
from elasticsearch import Elasticsearch
import logging
log_status={}

config = configparser.ConfigParser()

config.read('./config/config.ini')
es_index=config["ELASTICSEARCH"]["es_index"]
doc_type=config["ELASTICSEARCH"]["doc_type"]
host_name_=config["ELASTICSEARCH"]["host_name"]



logging.info('Connecting to ES host')
es_host = Elasticsearch(hosts=host_name_,use_ssl=False, ca_certs=certifi.where())

#write the json object results in Elastic search index which would be used from UI for async fetch

def index_in_es(ID,result):
    result['time_stamp']=datetime.now()
    try:
        res = es_host.index(index=es_index, doc_type=doc_type, id=ID, body=result)
        log_status['method'] = 'helper.write_result_to_es.index_in_es'
        log_status['status'] = 'Success'
        return (res['result'])
    except Exception as e:
        print(e)
        logging.debug('Elastic Search Indexing fail')
        log_status['method'] = 'helper.write_result_to_es.index_in_es'
        log_status['status'] = 'Failed'
        return 'Failed'


