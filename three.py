import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import difflib

# Define InfluxDB connection parameters
token = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
org = "Temasek Polytechnic"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "Smart Washroom"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

def queries():
    hours = input("Enter the time period in hours (e.g., 24, 48, etc.): ")
    query = f"""
        from(bucket: "Smart Washroom")
        |> range(start: -{hours}h)
        |> filter(fn: (r) => r._measurement == "environmental_data" and (r.location == "location_A" or r.location == "location_B"))
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> sort(columns:["_time"], desc: true)
    """
    data = client.query_api().query_data_frame(org=org, query=query)
    print(data)
    return data

def grade_variable(variable, value):
    if variable == 'temperature':
        if value >= 24.0:
            return 'Good'
        elif 20.0 <= value < 24.0:
            return 'Average'
        else:
            return 'Poor'
    elif variable == 'humidity':
        if value >= 60:
            return 'Good'
        elif 40 <= value < 60:
            return 'Average'
        else:
            return 'Poor'
    elif variable == 'light_intensity':
        if value >= 80.0:
            return 'Good'
        elif 50.0 <= value < 80.0:
            return 'Average'
        else:
            return 'Poor'
    elif variable == 'soap_level':
        if value >= 80.0:
            return 'Good'
        elif 60.0 <= value < 80.0:
            return 'Average'
        else:
            return 'Poor'
    elif variable == 'toilet_roll_usage':
        if value >= 60.0:
            return 'Good'
        elif 20.0 <= value < 60.0:
            return 'Average'
        else:
            return 'Poor'
    elif variable == 'people_counter':
        if value <= 10:
            return 'Good'
        elif 10 < value <= 25:
            return 'Average'
        else:
            return 'Poor'
    elif variable == 'ammonia_level':
        if value <= 0.20:
            return 'Good'
        elif 0.20 < value <= 0.30:
            return 'Average'
        else:
            return 'Poor'
    else:
        return 'Unknown variable'

def calculate_cleanliness_score(row):
    weights = {
        'temperature': 15,
        'humidity': 15,
        'light_intensity': 15,
        'soap_level': 20,
        'toilet_roll_usage': 10,
        'people_counter': 10,
        'ammonia_level': 15
    }

    grading_scores = {
        'Good': 90.0,
        'Average': 70.0,
        'Poor': 50.0
    }

    total_score = 0
    for column, weight in weights.items():
        try:
            score_range = grading_scores[row[column]]
            total_score += score_range * weight
            print(f"Row: {row}, Column: {column}, Score Range: {score_range}, Total Score: {total_score}")
        except KeyError as e:
            print(f"KeyError: {e} for column: {column} with row: {row}")
    return total_score

def main():
    datas = queries()
    df = pd.DataFrame(datas)
    # Check if 'people_counter' column exists in the DataFrame
    if 'people_counter' in df.columns:
    # Access 'people_counter' column for the row labeled 'result'
     if 'result' in df.index:
        try:
            value = df.loc['result', 'people_counter']
            # Process the 'people_counter' value
            print(value)  # or perform other operations
        except KeyError:
            print("KeyError: 'people_counter' column value not found for the 'result' row.")
     else:
        print("Row 'result' not found in the DataFrame.")
    else:
     print("'people_counter' column not found in the DataFrame.")



    # for column in df.columns:
    #     if column not in ['_time', '_result', '_table', '_start', '_measurement']:
    #         df[f'{column}_grade'] = df[column].apply(lambda value: grade_variable(column, value))
    
    # df['cleanliness_score'] = df.apply(calculate_cleanliness_score, axis=1)

if __name__ == "__main__":
    main()
