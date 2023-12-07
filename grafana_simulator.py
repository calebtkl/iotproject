import  time
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime
import random
token = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
org = "Temasek Polytechnic"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"
database="Smart Washroom"


client = InfluxDBClient3(host=host, token=token, org=org)
min = 20
max = 35
min1= 1
max1=50

min2=0.00
max2=100.00
min3=0.00
max3=100.00
min4=0.0
max4=1.0
min5=0.00
max5=0.50
min6=10
max6=60
all_fields= ["temperature","humidity","toilet_roll_usage","people_counter","light_intensity","soap_level","ammonia_level"]

while True:
    random_value = random.uniform(min, max) #temp
    random_value1 = random.randint(min1, max1) #people
    random_value2 = random.uniform(min2, max2)#light inten
    random_value3 = random.uniform(min3, max3)#toilet roll
    random_value4 = random.uniform(min4, max4)#soap
    random_value5 = random.uniform(min5, max5)#ammonia
    random_value6 = random.randint(min6, max6)#humidity
    random_value7 = random.uniform(min, max)
    random_value8 = random.randint(min1, max1)
    random_value9 = random.uniform(min2, max2)
    random_value10 = random.uniform(min3, max3)
    random_value11 = random.uniform(min4, max4)
    random_value12= random.uniform(min5, max5)
    random_value13= random.randint(min6, max6)
      
    data = {
    "location_A": {
    
        "temperature": {
            "sensor": "temperature",
            "value": random_value
        },
        "people_counter": {
            "sensor": "people_counter",
            "value": random_value1
        },
        "light_intensity": {
            "sensor": "light_intensity",
            "value": random_value2
        },
        "toilet_roll_usage": {
            "sensor": "toilet_roll_usage",
            "value": random_value3  # Assuming percentage or count of used toilet rolls
        },
        "soap_level": {
            "sensor": "soap_level",
            "value": random_value4  # Assuming a scale from 0 to 1 or 0 to 100%
        },
        "ammonia_level": {
            "sensor": "ammonia_level",
            "value":random_value5  # Assuming a scale or concentration measurement
        },
        "humidity": {
            "sensor": "humidity",
            "value": random_value6 # Assuming percentage humidity
        }
    },
    
    
    "location_B": {
        
        "temperature": {
            "sensor": "temperature",
            "value": random_value7
        },
        "people_counter": {
            "sensor": "people_counter",
            "value": random_value8
        },
        "light_intensity": {
            "sensor": "light_intensity",
            "value": random_value9
        },
        "toilet_roll_usage": {
            "sensor": "toilet_roll_usage",
            "value": random_value10  # Assuming percentage or count of used toilet rolls
        },
        "soap_level": {
            "sensor": "soap_level",
            "value": random_value11  # Assuming a scale from 0 to 1 or 0 to 100%
        },
        "ammonia_level": {
            "sensor": "ammonia_level",
            "value":random_value12  # Assuming a scale or concentration measurement
        },
        "humidity": {
            "sensor": "humidity",
            "value":random_value13 # Assuming percentage humidity
        },
        
    }
}


# Loop through data to create points
    for location_key, location_data in data.items():
        point = Point("environmental_data").tag("location", location_key)
    
        for field in all_fields:
            if field in location_data:
            # If the field exists for the location, add its data to the point
                point.field(field, location_data[field]['value'])
            else:
            # If the field doesn't exist for the location, add a placeholder or default value
                point.field(field, None)  # You can set a default value or None depending on your use case
    
    # Set time (optional, using current time here)
        point.time(datetime.utcnow())
          
          # Add the point to the batch list

        client.write(database=database, record=point)
        time.sleep(5) # separate points by 1 second

        print("Complete. Return to the InfluxDB UI.")



