#!/usr/bin/env python
import csv
import numpy as np


country_region_map = {
    "ESP" : "EU",
    "DEU" : "EU",
    "GBR" : "EU",
    "FRA" : "EU",
    "ITA" : "EU",
    "USA" : "US",
    "IND" : "IN"
}


def fetch_weights_local_gender(country, script):
    weights_dict = {}
    weights_dict[str(country)] = {}
    BASE_PATH = "/Users/shreyajain/PycharmProjects/Work/InSights/Back-end/Docker_Container/Data/Weights/" + script + "/"
    # BASE_PATH = "/Back-end/Docker_Container/Data/Weights/"
    FILE_PATH = BASE_PATH + country_region_map[country] + "/weights.csv"
    with open(FILE_PATH, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            weight = float(row[0])
            countryScript = row[1]
            region_type = row[2]
            if str(country) == str(countryScript):
                weights_dict[str(country)][region_type] = weight
            # if (country in weights_dict):
            #     weights_dict[country][region_type] = weight
            # else:
            #     weights_dict[str(country)] = {region_type: weight}
    # print ("weights_dict ", weights_dict[str(country)])
    weight_city, weight_region, weight_province, weight_country = weights_dict[str(country)]["city"], weights_dict[str(country)]["region"], weights_dict[str(country)]["province"], weights_dict[str(country)]["country"]
    # weight_city, weight_region, weight_province, weight_country = 0.1842805299, 0.3551745143, 0.3605449558, 0.1
    return np.array([weight_city,weight_region,weight_province,weight_country])



def fetch_weights_local_age(country, script):
    weights_dict = {}
    weights_dict[str(country)] = {}
    weights_dict[str(country)]["18_24"] = {}
    weights_dict[str(country)]["25_34"] = {}
    weights_dict[str(country)]["35_44"] = {}
    weights_dict[str(country)]["45_54"] = {}
    weights_dict[str(country)]["55_64"] = {}
    weights_dict[str(country)]["65_above"] = {}
    BASE_PATH = "/Users/shreyajain/PycharmProjects/Work/InSights/Back-end/Docker_Container/Data/Weights/" + script + "/"
    # BASE_PATH = "/Back-end/Docker_Container/Data/Weights/"
    FILE_PATH = BASE_PATH + country_region_map[country] + "/weights.csv"
    with open(FILE_PATH, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            weight = float(row[0])
            countryScript = row[1]
            age_type = row[2]
            region_type = row[3]
            if str(country) == str(countryScript):
                weights_dict[str(country)][age_type][region_type] = weight
    return weights_dict

