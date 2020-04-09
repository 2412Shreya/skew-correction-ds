import configparser
import pika
import json

from consumptionFromQueue import callback

input = {
  "qid" : 1,
  "country_code": "ESP",
  "query_type" : "impressions",
    "script" : "Gender",
  "attribute_matrix"
  : [{
  "attribute_value" : "Consumer",
    "country_ratio_sum":"123647.0856846571",
    "region_ratio_sum": "308559.16019934416",
    "city_ratio_sum": "309918.96382790804",
    "province_ratio_sum": "340467.78478115797",
    "country_status_sum": "79501",
    "region_status_sum": "377797",
    "city_status_sum": "356455",
    "province_status_sum":  "402020",
    "counts" : "3564557"
    },
      {
    "attribute_value" : "Enterprise",
    "country_ratio_sum":"123647.0856846571",
    "region_ratio_sum": "308559.16019934416",
    "city_ratio_sum": "309918.96382790804",
    "province_ratio_sum": "340467.78478115797",
    "country_status_sum": "79501",
    "region_status_sum": "377797",
    "city_status_sum": "356455",
    "province_status_sum":  "402020",
    "counts" : "3564557"

      }

    ]

}



input_json = json.dumps(input)

config = configparser.ConfigParser()
config.read('./config/config.ini')
queue_name=config["EXTERNAL.QUEUE"]["queue_name"]
queue_host_name=config["EXTERNAL.QUEUE"]["queue_host_name"]
user=config["EXTERNAL.QUEUE"]["user"]
password=config["EXTERNAL.QUEUE"]["password"]
#connection = pika.BlockingConnection(pika.ConnectionParameters(host=queue_host_name))
credentials = pika.PlainCredentials(user, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=queue_host_name,credentials=credentials))
channel = connection.channel()
print (queue_name)
channel.queue_declare(queue=queue_name,durable=True)
channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body=input_json)
print(" [x] Sent '")

try:
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue_name,callback)
except Exception as exp:
   print (exp)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()