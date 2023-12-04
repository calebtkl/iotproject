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

missing_values = data.isnull().sum()

# Check if there are any missing values in the dataset
if missing_values.any():
    # Handling Missing Values
    # Fill missing values with the mean of the column
    data.fillna(data.mean(), inplace=True)

    # Handling Duplicates
    # Identify duplicates
    print(data.duplicated().sum())  # Count of duplicate rows

    # Drop duplicate rows
    data.drop_duplicates(inplace=True)

    # Dealing with Outliers (example: using z-score)
    z_scores = stats.zscore(data)
    abs_z_scores = abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    data = data[filtered_entries]

    # Normalization and Scaling
    scaler = StandardScaler()
    data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

    min_max_scaler = MinMaxScaler()
    data = pd.DataFrame(min_max_scaler.fit_transform(data), columns=data.columns)
else:
    # Drop duplicate rows
    data.drop_duplicates(inplace=True)

    numeric_data = data.select_dtypes(include=[float, int]).columns.tolist()  # Selecting only numeric columns

# Calculating z-scores for numeric columns
    z_scores = stats.zscore(numeric_data)
    abs_z_scores = abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    numeric_data = numeric_data[filtered_entries]

    # Normalization and Scaling
    scaler = StandardScaler()
    numeric_data = pd.DataFrame(scaler.fit_transform(numeric_data), columns=data.columns)

    min_max_scaler = MinMaxScaler()
    numeric_data = pd.DataFrame(min_max_scaler.fit_transform(numeric_data), columns=data.columns)

# Now, the data has undergone various cleaning operations if missing values were present
print(numeric_data.head())  # Display the cleaned data