#!/usr/bin/env python

import collections, functools, operator



def prepareGenderSkewInput(string_query):
    attribute_list = []
    for row in string_query:
        temp_dict = {key: row[key] for key in ["attribute_value", "country_ratio_sum", "region_ratio_sum", "city_ratio_sum",\
                                               "province_ratio_sum", "country_status_sum", "region_status_sum", "city_status_sum", "province_status_sum"]}
        attribute_list.append(temp_dict)
    # print ("attribute_list", attribute_list)
    return attribute_list



def prepareAgeSkewInput(string_query):
    attribute_list = []
    for d in string_query:
        del_list = ["attribute_value", "country_ratio_sum", "region_ratio_sum", "city_ratio_sum", \
         "province_ratio_sum", "country_status_sum", "region_status_sum", "city_status_sum", "province_status_sum"]
        for i in del_list:
            del d[i]
        for k, v in d.items():
            d[k] = float(v)

    attribute_dict = dict(functools.reduce(operator.add,
                                   map(collections.Counter, string_query)))
    attribute_dict["attribute_value"] = "zeocore"

    attribute_list.append(attribute_dict)
    return attribute_list


