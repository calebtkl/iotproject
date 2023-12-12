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

def calculate_cleanliness_score(row):
    weights = {
        'temperature': 0.15,
        'humidity': 0.15,
        'light_intensity': 0.15,
        'soap_level': 0.20,
        'toilet_roll_usage': 0.10,
        'people_counter': 0.10,
        'ammonia_level': 0.15
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
        except KeyError:
            # Handle missing values or columns if needed
            pass
    
    # Calculate an adjusted score based on 'people_counter' values
    people_counter_weight = weights['people_counter']
    # Assuming 'people_counter' is one of the columns in your DataFrame 'row'
    people_counter_value = row['people_counter']
    people_counter_score = 100 if people_counter_value <= 10 else 50  # Example grading
    
    # Add 'people_counter' score to the total score
    total_score += people_counter_score * people_counter_weight

    return total_score

def main():
    datas = queries()
    df = pd.DataFrame(datas)
    
    # Check if 'people_counter' column exists in the DataFrame
    if 'people_counter' in df.columns:
        # Apply cleanliness score calculation to each row
        df['cleanliness_score'] = df.apply(calculate_cleanliness_score, axis=1)
        print(df[['people_counter', 'cleanliness_score']])  # Display people_counter and cleanliness score

if __name__ == "__main__":
    main()