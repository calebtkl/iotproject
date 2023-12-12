import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from io import BytesIO

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Define InfluxDB connection parameters
token = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
org = "Temasek Polytechnic"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "Smart Washroom"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

def queries():
    #hours = input("Enter the time period in hours (e.g., 24, 48, etc.): ")
    hours = 50
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
        'temperature': 0.25,
        'humidity': 0.15,
        'light_intensity': 0.05,
        'soap_level': 0.05,
        'toilet_roll_usage': 0.05,
        'people_counter': 0.20,
        'ammonia_level': 0.25
    }

    grading_scores = {
        'Good': 90.0,
        'Average': 70.0,
        'Poor': 50.0
    }

    total_score = 0
    for column, weight in weights.items():
        try:
            value = row[column]
            if value is not None:  # Handling None or missing values
                if column == 'temperature':
                    if value >= 24:
                        score = grading_scores['Good']
                    elif 20 <= value < 24:
                        score = grading_scores['Average']
                    else:
                        score = grading_scores['Poor']
                elif column == 'humidity':
                    if value >= 60:
                        score = grading_scores['Good']
                    elif 40 <= value < 60:
                        score = grading_scores['Average']
                    else:
                        score = grading_scores['Poor']
                elif column == 'light_intensity':
                    if value >= 80:
                        score = grading_scores['Good']
                    elif 50 <= value < 80:
                        score = grading_scores['Average']
                    else:
                        score = grading_scores['Poor']
                elif column == 'soap_level':
                    if value >= 80:
                        score = grading_scores['Good']
                    elif 60 <= value < 80:
                        score = grading_scores['Average']
                    else:
                        score = grading_scores['Poor']
                elif column == 'toilet_roll_usage':
                    if value >= 60:
                        score = grading_scores['Good']
                    elif 20 <= value < 60:
                        score = grading_scores['Average']
                    else:
                        score = grading_scores['Poor']
                elif column == 'people_counter':
                    if value <= 10:
                        score = grading_scores['Good']
                    elif 10 < value <= 25:
                        score = grading_scores['Average']
                    else:
                        score = grading_scores['Poor']
                elif column == 'ammonia_level':
                    if value <= 0.20:
                        score = grading_scores['Good']
                    elif 0.20 < value <= 0.30:
                        score = grading_scores['Average']
                    else:
                        score = grading_scores['Poor']
                else:
                    # For any other columns not specified, handle accordingly
                    score = grading_scores['Average']  # Example default grading

                total_score += score * weight
                
        except KeyError:
            # Handle missing values or columns if needed
            pass
    
    return total_score




def process_cleanliness(update, context):
    datas = queries()
    df = pd.DataFrame(datas)
    
    # Check if all relevant columns exist in the DataFrame
    relevant_columns = ['temperature', 'humidity', 'light_intensity', 'soap_level', 'toilet_roll_usage', 'people_counter', 'ammonia_level']
    if all(col in df.columns for col in relevant_columns):
        # Apply cleanliness score calculation to each row
        df['cleanliness_score'] = df.apply(calculate_cleanliness_score, axis=1)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="One or more relevant columns not found in the DataFrame.")
        return
    threshold = 35  # Set your threshold value here
    consecutive_count = 0
    for score in df['cleanliness_score'].iloc[::-1]:  # Loop through scores in reverse order
        if score < threshold:
            consecutive_count += 1
        else:
            consecutive_count = 0  # Reset count if the score is above the threshold
        
        if consecutive_count >= 3:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Cleanliness score has dropped below the threshold for 10 consecutive readings!")
            break  # Exit loop if condition met
    # End of process message
    context.bot.send_message(chat_id=update.effective_chat.id, text="Process completed successfully.")




def train_machine_learning_model(df, features, target_column):
    X = df[features]
    y = df[target_column]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

    return model





def plotscattergraph(df):
    x = df['ammonia_level']
    y = df['temperature']
    cleanliness = df['cleanliness_score']

    # Creating the scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, c=cleanliness, cmap='viridis', alpha=0.7)
    plt.colorbar(label='Cleanliness Score')
    plt.xlabel('Ammonia Level')
    plt.ylabel('Temperature')
    plt.title('Cleanliness with Ammonia Level and Temperature')
    plt.grid(True)

    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.show()

    return buffer





def plotlinegraph(df):
    df['_time'] = pd.to_datetime(df['_time'])
    df = df.sort_values('_time')

    # Plotting cleanliness score against time
    plt.figure(figsize=(10, 6))
    plt.plot(df['_time'], df['cleanliness_score'], label='Cleanliness Score')

    # Customize the graph
    plt.xlabel('Time')
    plt.ylabel('Cleanliness Score')
    plt.title('Cleanliness Score Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
 


    plt.show()

    return buffer


def main1():
    datas = queries()
    df = pd.DataFrame(datas)
    
    # Check if all relevant columns exist in the DataFrame
    relevant_columns = ['temperature', 'humidity', 'light_intensity', 'soap_level', 'toilet_roll_usage', 'people_counter', 'ammonia_level']
    if all(col in df.columns for col in relevant_columns):
        # Apply cleanliness score calculation to each row
        df['cleanliness_score'] = df.apply(calculate_cleanliness_score, axis=1)
        
     
    else:
        print("One or more relevant columns not found in the DataFrame.")

    
    # Call the machine learning function here
    # train_machine_learning_model(df,[  'soap_level', 'toilet_roll_usage', 'people_counter'], 'temperature')
    # plotscattergraph(df)
    # plotlinegraph(df)
    # End of process message

    print("Process completed successfully.")


if __name__ == '__main__':
    main1()