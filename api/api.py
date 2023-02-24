import pymongo
from collections import ChainMap
from pymongo import MongoClient
from datetime import datetime, timedelta

cluster = MongoClient(
    "mongodb+srv://growbox:1UDS6vKkwpzFCIuW@cluster0.r8wot.mongodb.net/?retryWrites=true&w=majority")
db = cluster["growbox"]

config = db["config"]
temperature = db["temperature"]
humidity = db["humidity"]

default_config = {
    "_id": "config_file",
    "start": {"hour": 0, "minute": 0},
    "end": {"hour": 0, "minute": 0},
    "is_running": False,
    "period": 0,
    "humidity_ranges": {
        "vegetative": {
            "humidity_min": "60",
            "humidity_max": "80"
        },
        "flowering": {
            "humidity_min": "45",
            "humidity_max": "55"
        }
    },
    "current_day": 0,
    "current_v_day": 0,
    "current_f_day": 0

}
humidity_report_day = [
    {
        "timestamp": datetime.now(),
        "value": 63.5,
        "time_of_the_day": "day"
    },
    {
        "timestamp": datetime.now(),
        "value": 65.5,
        "time_of_the_day": "day"
    },
    {
        "timestamp": datetime.now(),
        "value": 75.5,
        "time_of_the_day": "day"
    },
    {
        "timestamp": datetime.now(),
        "value": 77.5,
        "time_of_the_day": "day"
    },
    {
        "timestamp": datetime.now(),
        "value": 72.5,
        "time_of_the_day": "day"
    },
    {
        "timestamp": datetime.now(),
        "value": 62.5,
        "time_of_the_day": "day"
    }
]

humidity_report_night = [
    {
        "timestamp": datetime.now(),
        "value": 63.5,
        "time_of_the_day": "night",
    },
    {
        "timestamp": datetime.now(),
        "value": 65.5,
        "time_of_the_day": "night",
    },
    {
        "timestamp": datetime.now(),
        "value": 75.5,
        "time_of_the_day": "night",
    },
    {
        "timestamp": datetime.now(),
        "value": 77.5,
        "time_of_the_day": "night",
    },
    {
        "timestamp": datetime.now(),
        "value": 72.5,
        "time_of_the_day": "night",
    },
    {
        "timestamp": datetime.now(),
        "value": 62.5,
        "time_of_the_day": "night",
    }
]
temperature_report_day = [
    {
        "timestamp": datetime.now(),
        "value": 25.5,
        "time_of_the_day": "day",
    },
    {
        "timestamp": datetime.now(),
        "value": 24.5,
        "time_of_the_day": "day"
    },
    {
        "timestamp": datetime.now(),
        "value": 28,
        "time_of_the_day": "day"
    },
    {
        "timestamp": datetime.now(),
        "value": 27.5,
        "time_of_the_day": "day"
    },
    {
        "timestamp": datetime.now(),
        "value": 26,
        "time_of_the_day": "day"
    },
    {
        "timestamp": datetime.now(),
        "value": 22.5,
        "time_of_the_day": "day"
    }
]

temperature_report_night = [
    {
        "timestamp": datetime.now(),
        "value": 25.5,
        "time_of_the_day": "night",
    },
    {
        "timestamp": datetime.now(),
        "value": 24.5,
        "time_of_the_day": "night"
    },
    {
        "timestamp": datetime.now(),
        "value": 28,
        "time_of_the_day": "night"
    },
    {
        "timestamp": datetime.now(),
        "value": 27.5,
        "time_of_the_day": "night"
    },
    {
        "timestamp": datetime.now(),
        "value": 26,
        "time_of_the_day": "night"
    },
    {
        "timestamp": datetime.now(),
        "value": 22.5,
        "time_of_the_day": "night"
    }
]


class Api():
    def __init__(self):
        pass

    def set_default_config(self, default):
        try:
            config.insert_one(default)
        except Exception as error:
            print(type(error))

    def get_config(self):
        try:
            result = config.find_one({"_id": "config_file"})
            print(result)
            return result
        except Exception as error:
            print(type(error))

    def update_config(self, obj):
        try:
            config.update_one({"_id": "config_file"}, {"$set": obj})
        except Exception as error:
            print(type(error))

    def increment_day(self, period):
        print("INCREMENT")
        try:
            config.update_one({"_id": "config_file"}, {
                "$inc": {"current_day": 1, period: 1}})
        except Exception as error:
            print(type(error))

    def get_temperature(self):
        try:
            temp = temperature.find({})
            return temp
        except Exception as error:
            print(type(error))

    def insert_temperature(self):
        try:
            temperature.insert_many(
                temperature_report_day + temperature_report_night)
        except Exception as error:
            print(type(error))

    def get_humidity(self):
        try:
            temp = temperature.find({})
            return temp
        except Exception as error:
            print(type(error))

    def insert_humidity(self):
        try:
            humidity.insert_many(humidity_report_day + humidity_report_night)
        except Exception as error:
            print(type(error))


#api = Api()
# temperature.delete_many({})
# humidity.delete_many({})
# config.delete_many({})

# api.insert_temperature()
# api.insert_humidity()
# api.set_default_config(default_config)
#api.update_config({"started_at": datetime.now() - timedelta(days=4)})
#                  "start": {"hour": 7, "minute": 25}})
# api.increment_day("current_v_day")
# api.set_default_config()
