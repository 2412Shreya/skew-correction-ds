#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import subprocess
import csv


log_status = {}



def weights_redistribution(scores_dict, weights_dict, country_status_sum, region_status_sum, city_status_sum, province_status_sum):
    counts_array = np.array([city_status_sum, region_status_sum, province_status_sum, country_status_sum])
    # weights_array = np.array([0.6,0.2,0.1,0.1])
    # weights_array = fetch_weights(country)
    zero_indices = np.ndarray.tolist(np.where(counts_array == 0)[0])
    # print ("weights_dict ", weights_dict)
    weights_array = np.array([weights_dict['city'], weights_dict['region'], weights_dict['province'], weights_dict['country']])
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




def row_calculation(country, ratios_18_24, ratios_25_34, ratios_35_44, ratios_45_54, ratios_55_64, ratios_65_above, \
                                                     country_status_sum, region_status_sum, city_status_sum, province_status_sum, weights_dict):

    age_groups = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    age_map_scores = {"18-24" : ratios_18_24, "25-34" : ratios_25_34, "35-44": ratios_35_44, "45-54" : ratios_45_54, "55-64" : ratios_55_64, "65+" : ratios_65_above}
    age_map_weights = {"18-24" : "18_24", "25-34" : "25_34", "35-44": "35_44", "45-54" : "45_54", "55-64" : "55_64", "65+" : "65_above"}
    scores = {}

    for age in age_groups:
        # print ("scores ", age_map_scores[age])
        # print ("weights_dict ", weights_dict[str(country)][age_map_weights[age]])
        weight_city, weight_region, weight_province, weight_country  = weights_redistribution(age_map_scores[age],  weights_dict[str(country)][age_map_weights[age]], country_status_sum, region_status_sum, city_status_sum, province_status_sum)
        # weight_city, weight_region, weight_province, weight_country = weights_redistribution(country, country_status_sum, region_status_sum, city_status_sum, province_status_sum)
        updated_score = weight_city * (age_map_scores[age]["city_ratio_sum"]/city_status_sum ) + weight_region*(age_map_scores[age]["region_ratio_sum"]/region_status_sum) + \
                    weight_province*(age_map_scores[age]["province_ratio_sum"]/province_status_sum) + weight_country*(age_map_scores[age]["country_ratio_sum"]/country_status_sum)
        scores[age] = updated_score

    total = sum(scores.values(), 0.0)
    newScores = {k: (v / total)*100 for k, v in scores.items()}
    return newScores


def mainFunction(attribute_list, country, query_type, weights_dict):
    # df = pd.DataFrame.from_records(attribute_matrix)
    # header = df.iloc[0]
    # headers = header.tolist()
    # df = pd.DataFrame(attribute_matrix, columns=headers)
    # dfnew = df.iloc[1:]
    result = {}
    # print ("df ", df)
    for row in attribute_list:
        value = row['attribute_value']
        ratios_18_24 = {
                        "country_ratio_sum": float(row['18_24_country_ratio_sum']),
                        "region_ratio_sum": float(row['18_24_region_ratio_sum']),
                        "province_ratio_sum": float(row['18_24_province_ratio_sum']),
                        "city_ratio_sum": float(row['18_24_city_ratio_sum'])
                        }
        ratios_25_34 = {
            "country_ratio_sum": float(row['25_34_country_ratio_sum']),
            "region_ratio_sum": float(row['25_34_region_ratio_sum']),
            "province_ratio_sum": float(row['25_34_province_ratio_sum']),
            "city_ratio_sum": float(row['25_34_city_ratio_sum'])
        }
        ratios_35_44 = {
            "country_ratio_sum": float(row['35_44_country_ratio_sum']),
            "region_ratio_sum": float(row['35_44_region_ratio_sum']),
            "province_ratio_sum": float(row['35_44_province_ratio_sum']),
            "city_ratio_sum": float(row['35_44_city_ratio_sum'])
        }
        ratios_45_54 = {
            "country_ratio_sum": float(row['45_54_country_ratio_sum']),
            "region_ratio_sum": float(row['45_54_region_ratio_sum']),
            "province_ratio_sum": float(row['45_54_province_ratio_sum']),
            "city_ratio_sum": float(row['45_54_city_ratio_sum'])
        }
        ratios_55_64 = {
            "country_ratio_sum": float(row['55_64_country_ratio_sum']),
            "region_ratio_sum": float(row['55_64_region_ratio_sum']),
            "province_ratio_sum": float(row['55_64_province_ratio_sum']),
            "city_ratio_sum": float(row['55_64_city_ratio_sum'])
        }
        ratios_65_above = {
            "country_ratio_sum": float(row['65+_country_ratio_sum']),
            "region_ratio_sum": float(row['65+_region_ratio_sum']),
            "province_ratio_sum": float(row['65+_province_ratio_sum']),
            "city_ratio_sum": float(row['65+_city_ratio_sum'])

        }
        country_status_sum = float(row['country_age_status_sum'])
        region_status_sum = float(row['region_age_status_sum'])
        city_status_sum = float(row['city_age_status_sum'])
        province_status_sum = float(row['province_age_status_sum'])
        func_score = row_calculation(country, ratios_18_24, ratios_25_34, ratios_35_44, ratios_45_54, ratios_55_64, ratios_65_above, \
                                                     country_status_sum, region_status_sum, city_status_sum, province_status_sum, weights_dict)


        # print ("func_score, ", func_score)
        result[value] = { "18-24": func_score["18-24"], "25-34" : func_score["25-34"], "35-44": func_score["35-44"], "45-54": func_score["45-54"], "55-64": func_score["55-64"], "65+": func_score["65+"]}
    log_status['method'] = 'Skew_Attribute.AgeSkew.mainFunction'
    log_status['status'] = 'Success'
    return result


