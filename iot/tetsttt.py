import os, time
from influxdb_client_3 import InfluxDBClient3, Point
import pandas


token = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
org = "Temasek Polytechnic"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"
database="Smart Washroom"

client = InfluxDBClient3(host=host, token=token, org=org)


query = """
from(bucket: "Smart Washroom")
    |> range(start: -24h)
    |> filter(fn: (r) => r._measurement == "environmental_data" and (r.location == "location_A" or r.location == "location_B"))
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> sort(columns:["_time"], desc: true)
"""
# Execute the query
table = client.query(query=query, database="Smart Washroom") 

# Convert to dataframe
df = table.to_pandas().sort_values(by="time")
print(df)