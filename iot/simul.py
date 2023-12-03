import os, time
from influxdb_client_3 import InfluxDBClient3
import pandas


token = os.environ.get("INFLUXDB_TOKEN")
org = "temasek poly"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"
client = InfluxDBClient3(host=host, token=token, org=org)
bucket="bong"




def query_influxdb():
   
   query = 'from(bucket: "bong") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "environmental_data")'
   pd = client.query(query=query, mode="pandas")
# Print the pandas DataFrame formatted as a Markdown table.
   print(pd.to_markdown())
   
# datacleaning.py

def clean_zero_values(data):
    # Remove entries with zero values for specific parameters
    cleaned_data = [
        entry for entry in data 
        if (
                entry.get('temperature') != 0 
            and entry.get('soap_level') != 0 
            and entry.get('humidity') != 0 
            and entry.get('people_counter') != 0 
            and entry.get('toilet_roll_usage') != 0 
            and entry.get('ammonia_level') != 0
             and entry.get('light_intensity') != 0
        )
    ]
    return cleaned_data

def remove_duplicates(cleaned_data):
    # Remove duplicate entries
    cleaned_data = []
    seen = set()
    for entry in cleaned_data:
        entry_tuple = (
            entry.get('temperature'), 
            entry.get('soap_level'), 
            entry.get('humidity'), 
            entry.get('people_counter'), 
            entry.get('toilet_roll_usage'), 
            entry.get('ammonia_level'),
            entry.get('light_intensity')
            
        )
        if entry_tuple not in seen:
            cleaned_data.append(entry)
            seen.add(entry_tuple)
    return cleaned_data

def remove_outliers(cleaned_data):
    # Remove outliers based on certain conditions for each variable
    cleaned_data = [
        entry for entry in cleaned_data
        if (
            entry.get('temperature') < 100  # Example condition for temperature
            and entry.get('soap_level') < 1000  # Example condition for soapLevel
            and entry.get('humidity') < 100  # Example condition for humidity
            and entry.get('people_counter') < 1000  # Example condition for peopleCounter
            and entry.get('toilet_roll_usage') < 50  # Example condition for toiletRoll
            and entry.get('ammonia_level') < 10# Example condition for ammoniaLevel
            and entry.get('light_intensity') < 1000
            # Add conditions for each variable based on your dataset and domain knowledge
        )
    ]
    return cleaned_data

# datacleaning.py

def impute_missing_values(cleaned_data):
    cleaned_data = cleaned_data.copy()  # Create a copy of the data to avoid modifying the original dataset

    # Example: Fill missing temperature values with the mean temperature of the dataset
    temperature_values = [entry.get('temperature') for entry in cleaned_data if entry.get('temperature') is not None]
    temperature_mean = sum(temperature_values) / len(temperature_values) if temperature_values else None

    # Example: Fill missing soapLevel values with the mean soapLevel of the dataset
    soap_values = [entry.get('soap_level') for entry in cleaned_data if entry.get('soap_level') is not None]
    soap_mean = sum(soap_values) / len(soap_values) if soap_values else None

    # Example: Fill missing humidity values with a predefined value (e.g., 50)
    humidity_default = 50

    # Example: Fill missing peopleCounter values with the median peopleCounter of the dataset
    people_values = [entry.get('people_counter') for entry in cleaned_data if entry.get('people_counter') is not None]
    people_median = sorted(people_values)[len(people_values) // 2] if people_values else None

    # Example: Fill missing toiletRoll values with the median toiletRoll of the dataset
    toilet_values = [entry.get('toilet_roll_usage') for entry in cleaned_data if entry.get('toilet_roll_usage') is not None]
    toilet_median = sorted(toilet_values)[len(toilet_values) // 2] if toilet_values else None

    # Example: Fill missing ammoniaLevel values with a predefined value (e.g., 0)
    ammonia_default = 0.02
    
    light_intensity_default = 500

    # Iterate through each entry and perform imputation if the value is missing
    for entry in cleaned_data:
        if entry.get('temperature') is None:
            entry['temperature'] = temperature_mean if temperature_mean is not None else 0

        if entry.get('soap_level') is None:
            entry['soap_level'] = soap_mean if soap_mean is not None else 0

        if entry.get('humidity') is None:
            entry['humidity'] = humidity_default

        if entry.get('people_counter') is None:
            entry['people_counter'] = people_median if people_median is not None else 0

        if entry.get('toilet_roll_usage') is None:
            entry['toilet_roll_usage'] = toilet_median if toilet_median is not None else 0

        if entry.get('ammonia_level') is None:
            entry['ammonia_level'] = ammonia_default
            
        if entry.get('light_intensity') is None:
            entry['light_intensity'] = ammonia_default

    return cleaned_data


def main():
    influx_data = query_influxdb()
    if influx_data:
        cleaned_data = clean_zero_values(influx_data)
        cleaned_data = remove_duplicates(cleaned_data)
        cleaned_data = remove_outliers(cleaned_data)
        cleaned_data = impute_missing_values(cleaned_data)
        
        # Further processing or analysis with the cleaned data
        for entry in cleaned_data:
            print(entry)  # Replace with your actual processing logic

if _name_ == '_main_':
    main()