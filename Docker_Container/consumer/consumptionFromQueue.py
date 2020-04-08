#!/usr/bin/env python

import json

import Skew_Attribute.GenderSkew as GenderSkew
import Skew_Attribute.AgeSkew as AgeSkew

import helper.utils as utils
import helper.dissectInputs as prepareInput
import logging
import subprocess, os
import numpy as np
import csv

from helper.writetoES import index_in_es



log_status = {}
logging.basicConfig(filename='../subscriber.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info('Creating A subscriber')



# callback function to consume data from the queue
def callback(ch, method, properties, body):
    # path = "/Users/shreyajain/PycharmProjects/Work/InSights/Back-end/Docker_Container/Data/Inputs/input_Age_Gender_skew.json"
    # body = open(path, "r")
    try:
        print("Process start:")
        body = body.decode("utf-8")
        # string_query = json.loads(body)['query'].lower()
        result = json.loads(body)
        string_query = result["attribute_matrix"]
        country_id = result["country_code"]
        qid = result["qid"]
        query_type = result["query_type"]
        script = result["script"]
        # print ( "string_query", string_query)
        skew_correction_result_json = {}
        output = {}
        if script == "Gender":
            weights_array = utils.fetch_weights_local_gender(country_id, script)
            output = GenderSkew.mainFunction(string_query, country_id, query_type, weights_array)
        elif script == "Age":
            weights_dict = fetch_weights_local_age(country_id, script)
            output = AgeSkew.mainFunction(string_query, country_id, query_type, weights_dict)
        elif script == "GenderAge":
            weights_array_gender = utils.fetch_weights_local_gender(country_id, "Gender")
            weights_dict_age = fetch_weights_local_age(country_id, "Age")
            attribute_list_gender = prepareInput.prepareGenderSkewInput(string_query)
            output_gender = GenderSkew.mainFunction(attribute_list_gender, country_id, query_type, weights_array_gender)
            attribute_list_age = prepareInput.prepareAgeSkewInput(string_query)
            output_age = AgeSkew.mainFunction(attribute_list_age, country_id, query_type, weights_dict_age)['zeocore']
            for k, v in output_gender.items():
                male_score = float(output_gender[k]['male'])*0.01
                female_score = float(output_gender[k]['female'])*0.01
                age_score = output_age[k]
                male_ratio = age_score*male_score
                female_ratio = age_score*female_score
                output[k] = { "male" : male_ratio,
                              "female" : female_ratio }

        print ("***************")
        print ("output ", output)
        skew_correction_result_json["output"] = output
        skew_correction_result_json["attribute_matrix"] = string_query
        skew_correction_result_json["country_code"] = country_id
        skew_correction_result_json["qid"] = qid
        skew_correction_result_json["query_type"] = query_type
        skew_correction_result_json["script"] = script

        status_ = (index_in_es(qid, skew_correction_result_json))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print ("result pushed")

        # logging
        log_status['method'] = "subscirber"
        log_status['status'] = "Success"

        logs = []
        logs_ = {}
        logs.append(log_status)


        id_ = qid + "LogS"
        logs_['logs'] = logs
        logs_['qid_'] = id_
        print('log_status:', logs_)

        status__ = (index_in_es(id_, logs_))
        print(status__)
        logging.info('Log status pushed')

        return status_
    except Exception as exp:
        print (exp)
        print ("input error message is:", body)
        return True



