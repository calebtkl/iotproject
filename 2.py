import influxdb_client 
from influxdb_client.client.write_api import SYNCHRONOUS
import time

import pandas as pd
import difflib

# Define InfluxDB connection parameters
token = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
org = "Temasek Polytechnic"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "Smart Washroom"

# Create an InfluxDB client object

valid_options = ["temperature", "humidity", "light intensity", "soap level", "people counter","ammonia level", "toilet roll usage"]  # Add more options as needed

hours = input("Enter the time period in hours (e.g., 24, 48, etc.): ")
variable = input("Enter the time period in hours (e.g.temperature, humidity, light intensity etc.):")

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Construct an InfluxDB query
query = f"""
from(bucket: "Smart Washroom")
    |> range(start: -{hours}h)
    |> filter(fn: (r) => r._measurement == "environmental_data" and (r.location == "location_A" or r.location == "location_B"))
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> sort(columns:["_time"], desc: true)
"""
# Query data from InfluxDB
data = client.query_api().query_data_frame(org=org, query=query)

# Check if the input matches a valid option
if variable in valid_options:
    print(f"Variable '{variable}' accepted.")
else:
    # Find the closest match using difflib's get_close_matches function
    closest_matches = difflib.get_close_matches(variable, valid_options, n=3, cutoff=0.5)  # Adjust cutoff as needed
    if closest_matches:
        variables = closest_matches[0]
       
        print(f"Variable '{variables}' accepted after filtering.")
        
        if variables  == "temperature" :

        # Extracting specific fields from the DataFrame
            temperatures = data[["temperature"]]
            print(temperatures)
    

        elif variables  == "humidity" :

         # Extracting specific fields from the DataFrame
            humidity = data[["humidity"]]
            print(humidity)
    
        elif variables == "light intensity" :

        # Extracting specific fields from the DataFrame
            lightintensity = data[["light_intensity"]]
            print(lightintensity)
    
        elif variables == "soap level" :

        # Extracting specific fields from the DataFrame
            soaplevel = data[["soap_level"]]
            print(soaplevel)
    
        elif variables == "toilet roll usage" :

        # Extracting specific fields from the DataFrame
            toilet = data[["toilet_roll_usage"]]
            print(toilet)
    
        elif variables == "ammonia level" :

        # Extracting specific fields from the DataFrame
            ammonia = data[["ammonia_level"]]
            print(ammonia)
    
    
        elif variables == "people counter" :

        # Extracting specific fields from the DataFrame
            people = data[["people_counter"]]
            print(people)

        else:
            print("no such variable")
        
        
        
    else:
        print("Invalid input.")
        
df=pd.DataFrame(data)

def grade_temperature(temp):
    if temp >= 24:
        return 'Good'
    elif 20 <= temp < 24:
        return 'Average'
    else:
        return 'Poor'
    
    
# Define grading functions for each variable
def grade_soap_level(soap_level):
    if soap_level >= 80:
        return 'Good'
    elif 60 <= soap_level < 80:
        return 'Average'
    else:
        return 'Poor'

def grade_light_intensity(light_intensity):
    if light_intensity >= 80:
        return 'Good'
    elif 50 <= light_intensity < 80:
        return 'Average'
    else:
        return 'Poor'

def grade_toilet_roll_usage(toilet_roll_usage):
    if toilet_roll_usage >= 60:
        return 'Good'
    elif 20 <= toilet_roll_usage < 60:
        return 'Average'
    else:
        return 'Poor'

def grade_people_counter(people_counter):
    if people_counter <= 10:
        return 'Good'
    elif 10 < people_counter <= 25:
        return 'Average'
    else:
        return 'Poor'

def grade_humidity(humidity):
    if humidity >= 60:
        return 'Good'
    elif 40 <= humidity < 60:
        return 'Average'
    else:
        return 'Poor'

def grade_temperature(temperature):
    if temperature >= 25:
        return 'Good'
    elif 20 <= temperature < 25:
        return 'Average'
    else:
        return 'Poor'

def grade_ammonia_level(ammonia_level):
    if ammonia_level <= 0.2:
        return 'Good'
    elif 0.2< ammonia_level <= 0.3:
        return 'Average'
    else:
        return 'Poor'


weights = {
    
    'temperature': 0.15,
    'humidity': 0.15,
    'light_intensity': 0.15,
    'soap_level': 0.2,
    'toilet_roll_usage': 0.1,
    'people_counter':0.1,
    'ammonia_level':0.15
    
    
}
    
# Define a mapping of temperature grades to cleanliness scores
grading_scores = {
    'Good': 90,  # Assign cleanliness scores for each grade
    'Average': 70,
    'Poor': 50
}

import influxdb_client 
from influxdb_client.client.write_api import SYNCHRONOUS
import time

import pandas as pd
import difflib

# Define InfluxDB connection parameters
token = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
org = "Temasek Polytechnic"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "Smart Washroom"

# Create an InfluxDB client object

valid_options = ["temperature", "humidity", "light intensity", "soap level", "people counter","ammonia level", "toilet roll usage"]  # Add more options as needed

hours = input("Enter the time period in hours (e.g., 24, 48, etc.): ")
variable = input("Enter the time period in hours (e.g.temperature, humidity, light intensity etc.):")

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Construct an InfluxDB query
query = f"""
from(bucket: "Smart Washroom")
    |> range(start: -{hours}h)
    |> filter(fn: (r) => r._measurement == "environmental_data" and (r.location == "location_A" or r.location == "location_B"))
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> sort(columns:["_time"], desc: true)
"""
# Query data from InfluxDB
data = client.query_api().query_data_frame(org=org, query=query)
print(data)

df=pd.DataFrame(data)


def test_variables():
# Check if the input matches a valid option
 if variable in valid_options:
    print(f"Variable '{variable}' accepted.")
 else:
    # Find the closest match using difflib's get_close_matches function
    closest_matches = difflib.get_close_matches(variable, valid_options, n=3, cutoff=0.5)  # Adjust cutoff as needed
    if closest_matches:
        variables = closest_matches[0]
       
        print(f"Variable '{variables}' accepted after filtering.")
        
        if variables  == "temperature" :

        # Extracting specific fields from the DataFrame
            temperatures = data[["temperature"]]
            print(temperatures)
    

        elif variables  == "humidity" :

         # Extracting specific fields from the DataFrame
            humidity = data[["humidity"]]
            print(humidity)
    
        elif variables == "light intensity" :

        # Extracting specific fields from the DataFrame
            lightintensity = data[["light_intensity"]]
            print(lightintensity)
    
        elif variables == "soap level" :

        # Extracting specific fields from the DataFrame
            soaplevel = data[["soap_level"]]
            print(soaplevel)
    
        elif variables == "toilet roll usage" :

        # Extracting specific fields from the DataFrame
            toilet = data[["toilet_roll_usage"]]
            print(toilet)
    
        elif variables == "ammonia level" :

        # Extracting specific fields from the DataFrame
            ammonia = data[["ammonia_level"]]
            print(ammonia)
    
    
        elif variables == "people counter" :

        # Extracting specific fields from the DataFrame
            people = data[["people_counter"]]
            print(people)

        else:
            print("no such variable")
        
        
        
    else:
        print("Invalid input.")
        


def grade_temperature(temp):
    if temp >= 24:
        return 'Good'
    elif 20 <= temp < 24:
        return 'Average'
    else:
        return 'Poor'
    
    
# Define grading functions for each variable
def grade_soap_level(soap_level):
    if soap_level >= 80:
        return 'Good'
    elif 60 <= soap_level < 80:
        return 'Average'
    else:
        return 'Poor'

def grade_light_intensity(light_intensity):
    if light_intensity >= 80:
        return 'Good'
    elif 50 <= light_intensity < 80:
        return 'Average'
    else:
        return 'Poor'

def grade_toilet_roll_usage(toilet_roll_usage):
    if toilet_roll_usage >= 60:
        return 'Good'
    elif 20 <= toilet_roll_usage < 60:
        return 'Average'
    else:
        return 'Poor'

def grade_people_counter(people_counter):
    if people_counter <= 10:
        return 'Good'
    elif 10 < people_counter <= 25:
        return 'Average'
    else:
        return 'Poor'

def grade_humidity(humidity):
    if humidity >= 60:
        return 'Good'
    elif 40 <= humidity < 60:
        return 'Average'
    else:
        return 'Poor'

def grade_temperature(temperature):
    if temperature >= 25:
        return 'Good'
    elif 20 <= temperature < 25:
        return 'Average'
    else:
        return 'Poor'

def grade_ammonia_level(ammonia_level):
    if ammonia_level <= 0.2:
        return 'Good'
    elif 0.2< ammonia_level <= 0.3:
        return 'Average'
    else:
        return 'Poor'


weights = {
    
    'temperature': 15,
    'humidity': 15,
    'light_intensity': 15,
    'soap_level': 20,
    'toilet_roll_usage': 10,
    'people_counter':10,
    'ammonia_level':15
    
    
}
    
# Define a mapping of temperature grades to cleanliness scores
grading_scores = {
    'Good': 90,  # Assign cleanliness scores for each grade
    'Average': 70,
    'Poor': 50
}

# Define cleanliness scoring function
def calculate_cleanliness_score(row):
    total_score = sum(row[feature+'_grade'] * weight for feature, weight in weights.items())
    return total_score

# Apply grading functions to respective columns in the DataFrame
df['soap_level_grade'] = df['soap_level'].apply(grade_soap_level)
df['light_intensity_grade'] = df['light_intensity'].apply(grade_light_intensity)
df['toilet_roll_usage_grade'] = df['toilet_roll_usage'].apply(grade_toilet_roll_usage)
df['people_counter_grade'] = df['people_counter'].apply(grade_people_counter)
df['humidity_grade'] = df['humidity'].apply(grade_humidity)
df['temperature_grade'] = df['temperature'].apply(grade_temperature)
df['ammonia_level_grade'] = df['ammonia_level'].apply(grade_ammonia_level)

# Calculate cleanliness scores for each row
df['cleanliness_score'] = df.apply(calculate_cleanliness_score, axis=1)

print(df)
    











    










