import influxdb_client 
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd


# Define InfluxDB connection parameters
token = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
org = "Temasek Polytechnic"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "Smart Washroom"

# Create an InfluxDB client object
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Construct an InfluxDB query
query = """
from(bucket: "Smart Washroom")
    |> range(start: -24h)
    |> filter(fn: (r) => r._measurement == "environmental_data" and (r.location == "location_A" or r.location == "location_B"))
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> sort(columns:["_time"], desc: true)
"""
# Query data from InfluxDB
data = client.query_api().query_data_frame(org=org, query=query)

# Print query results
print(data)

