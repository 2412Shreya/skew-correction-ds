#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import subprocess
import csv


log_status = {}



def weights_redistribution(country, country_status_sum, region_status_sum, city_status_sum, province_status_sum, weights_array):
    counts_array = np.array([city_status_sum, region_status_sum, province_status_sum, country_status_sum])
    # weights_array = np.array([0.6,0.2,0.1,0.1])
    # weights_array = fetch_weights(country)
    zero_indices = np.ndarray.tolist(np.where(counts_array == 0)[0])
    if len(zero_indices) > 0:
        sum_weights_num = weights_array[zero_indices].sum()
        sum_weights_den = 1 - sum_weights_num
        uplift_factor = 1+ sum_weights_num/sum_weights_den
        for i in range(0,4):
            if counts_array[i] != 0:
                weights_array[i] *= uplift_factor
            else:
                weights_array[i] = 0
    return weights_array[0], weights_array[1], weights_array[2], weights_array[3]


def row_calculation_impressions(country, country_ratio_sum, country_status_sum, region_ratio_sum, region_status_sum, \
                        city_ratio_sum, city_status_sum, province_ratio_sum, province_status_sum, weights_array):
    weight_city, weight_region, weight_province, weight_country = weights_redistribution(country, country_status_sum, region_status_sum, city_status_sum, province_status_sum, weights_array)
    updated_score = weight_city * (city_ratio_sum/city_status_sum ) + weight_region*(region_ratio_sum/region_status_sum) + \
                    weight_province*(province_ratio_sum/province_status_sum) + weight_country*(country_ratio_sum/country_status_sum)
    # impressions equation, when update_score > 0.87818652849, it's male dominated and stretched linearly
    # if above then it's stretched towards females
    if updated_score <= 0.87818652849:
        func_score = 1.37259085432* updated_score
    else:
        func_score = 48.25* updated_score -34.1525
    if func_score > 19:
        func_score = 19
    elif func_score < 0.05263157894:
        func_score = 0.05263157894
    return func_score


def row_calculation_users(country, country_ratio_sum, country_status_sum, region_ratio_sum, region_status_sum, \
                        city_ratio_sum, city_status_sum, province_ratio_sum, province_status_sum, weights_array):
    weight_city, weight_region, weight_province, weight_country = weights_redistribution(country, country_status_sum, region_status_sum, city_status_sum, province_status_sum)
    updated_score = weight_city * (city_ratio_sum/city_status_sum ) + weight_region*(region_ratio_sum/region_status_sum) + \
                    weight_province*(province_ratio_sum/province_status_sum) + weight_country*(country_ratio_sum/country_status_sum)
    # users equation, when update_score > 0.76854922279, it's male dominated and stretched linearly
    # if above then it's stretched towards females
    if updated_score <= 0.76854922279:
        func_score = 1.30115283491*updated_score
    else:
        func_score = 48.25* updated_score -36.0825
    if func_score > 19:
        func_score = 19
    elif func_score < 0.05263157894:
        func_score = 0.05263157894
    return func_score


def mainFunction(attribute_list, country, query_type, weights_array):
    # df = pd.DataFrame.from_records(attribute_matrix)
    # header = df.iloc[0]
    # headers = header.tolist()
    # df = pd.DataFrame(attribute_matrix, columns=headers)
    # dfnew = df.iloc[1:]
    result = {}
    # print ("df ", df)
    for row in attribute_list:
        value = row['attribute_value']
        country_ratio_sum = float(row['country_ratio_sum'])
        country_status_sum = float(row['country_status_sum'])
        region_ratio_sum = float(row['region_ratio_sum'])
        region_status_sum = float(row['region_status_sum'])
        city_ratio_sum = float(row['city_ratio_sum'])
        city_status_sum = float(row['city_status_sum'])
        province_ratio_sum = float(row['province_ratio_sum'])
        province_status_sum = float(row['province_status_sum'])
        if query_type == "impressions":
            func_score = row_calculation_impressions(country, country_ratio_sum, country_status_sum, region_ratio_sum, region_status_sum, \
                        city_ratio_sum, city_status_sum, province_ratio_sum, province_status_sum, weights_array)
        else:
            func_score = row_calculation_users(country, country_ratio_sum, country_status_sum,
                                                          region_ratio_sum, region_status_sum, \
                                                          city_ratio_sum, city_status_sum, province_ratio_sum,
                                                          province_status_sum, weights_array)
        female_percentage = (func_score / (1 + func_score)) * 100
        male_percentage = 100 - female_percentage
        # print ("female % of ", value, ": ", female_percentage)
        result[value] = {"female" : female_percentage, "male" : male_percentage}
        # return female_percentage, male_percentage
    log_status['method'] = 'Skew_Attribute.GenderSkew.mainFunction'
    log_status['status'] = 'Success'
    return result


# obj = ratioCalculations()

# query_type = "impressions"

# Test Case 1
# attribute_matrix_consumer_type = [["attribute_vale","country_ratio_sum","country_status_sum","region_ratio_sum", "region_status_sum", "city_ratio_sum","city_status_sum","province_ratio_sum","province_status_sum"], \
#                                   ["Consumer", "123647.0856846571", "79501", "308559.16019934416", "377797", "309918.96382790804", "356455", "340467.78478115797", "402020"], \
#                                   ["Enterprise", "10762.858892560005", "6919", "16924.28680807352", "21517", "17218.86129885912", "20763", "18859.181734740734", "23391"]]



# mainFunction(attribute_matrix_consumer_type, "ESP", query_type, weights_array)
