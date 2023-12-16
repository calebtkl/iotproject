from telegram.ext import Updater, MessageHandler, Filters,CallbackContext, CommandHandler
import schedule
import time

#from report import query, plot_graph
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, ReplyKeyboardMarkup,ReplyKeyboardRemove, Bot
import influxdb_client 
from influxdb_client.client.write_api import SYNCHRONOUS
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

#hours = None  # Initialize the variable without a specific value

def start(update,context):
    user_name = update.message.from_user.first_name
    update.message.reply_text(f"Hi, {user_name}! I'm here to assist you.\n"
        "Here are the available commands:\n"
        "/graph - Generate a graph (scatter or line)\n"
        "/report - Generate a report\n"
        "/live - Get the link for live data\n")

def reply(update, context):
    
      if context.user_data.get('graph_selected'):
        # Graph generation logic...
      

        # Clear the flag for the next graph selection
        context.user_data['graph_selected'] = False
      else:
        keyboard = [['Scatter', 'Line']]
        update.message.reply_text(
            "Choose the type of graph:",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )
        context.user_data['graph_selected'] = True
      handle_graph(update, context)
    
   

   


def replies(update, context):
  
        # message = f"Please enter the time period of {hours} hours for the graph."
        # update.message.reply_text(message)
        # context.user_data['response_type_2'] = hours
        handle_report(update, context)


      
  
        
        
def live(update,context):
       
        hosted_url = 'https://calebtankaile7878.grafana.net/public-dashboards/f0500325a3834ed39b4d6d81ef390423'
        reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Open Link", url=hosted_url)]]
    )
        update.message.reply_text("Click the button to open the link:", reply_markup=reply_markup)


def static(update,context):
 
       
        hosted_url = 'https://mohammadnurzaharyan2710.grafana.net/public-dashboards/c56ffe2bab9f460a9f5153471436fefa?orgId=1&from=1702458897827&to=1702460693843 '
        reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Open Link", url=hosted_url)]]
    )
        update.message.reply_text("Click the button to open the link:", reply_markup=reply_markup)
   

def handle_report(update, context):
    
    chat_id = update.message.chat_id
    hours = update.message.text
    data = query()
    report = ""
    
    reports=generate_report(data,report)
    update.message.reply_text("Report generated hold up......")
    context.bot.send_document(chat_id=chat_id, document=open(reports, "rb"))

    # Remove the generated report file
    os.remove(reports)
    # Process data or generate report here

def handle_graph(update, context):
    
    # update.message.reply_text("Graph generated!")
    # if update.message.text.isdigit():
    #     hours = int(update.message.text)
    #     context.user_data['response_type_2'] = hours
    #     message = f"Please enter the time period of {hours} hours for the graph."
    #     update.message.reply_text(message)
    #     # Proceed with the graph generation or any other logic
    #     # handle_graph_logic(update, context)
    # else:
    #     update.message.reply_text("Please enter a valid integer for the time period.")
    # hours = update.message.text

    graph_type = update.message.text.lower()
    
   
    data = query()
    
 
     
    if graph_type == 'scatter':
            context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='graph generated',
            reply_markup=ReplyKeyboardRemove(),
            )
       
            image_path = 'scatter.png'
          
            plot_scatter(data, image_path)
    
            # Send the image to Telegram
            context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open(image_path, 'rb'))
    elif graph_type == 'line':
            context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='graph generated',
            reply_markup=ReplyKeyboardRemove(),
            )
       
            
            image_path = 'line.png'
        
            plot_line(data, image_path)
            
            
            # Send the image to Telegram
            context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open(image_path, 'rb'))
   

    

    
 
        
def query():
    # Define InfluxDB connection parameters
    token = "SckCRn0kqB-hwH4fmWtJvWOKihHLRWZo0zgsKoO71Yr7oURJENeqQCWcTlrVfkgqjWV1H6qku_WxdeTMwMcA9g=="
    org = "Temasek Polytechnic"
    url = "https://us-east-1-1.aws.cloud2.influxdata.com"
    database = "smart washroom"


    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

    
# from(bucket: "smart washroom")
#     |> range(start: 2023-01-01T00:00:00Z, stop: 2023-01-02T00:00:00Z)  // Replace with your desired start and stop time
#     |> filter(fn: (r) => r._measurement == "environmental_data" and (r.location == "location_A" or r.location == "location_B"))
#     |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
#     |> sort(columns:["_time"], desc: true)  
    query = f"""
from(bucket: "Smart Washroom")
    |> range(start: -50h)
    |> filter(fn: (r) => r._measurement == "environmental_data" and (r.location == "location_A" or r.location == "location_B"))
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> sort(columns:["_time"], desc: true)
"""
    # Query data from InfluxDB
    data = client.query_api().query_data_frame(org=org, query=query)
    columns_to_remove = ['result', 'table','_time','_start','_stop','_measurement']  # List of columns to be removed
    print(data)
    
# Dropping the specified columns
    data.drop(columns=columns_to_remove, inplace=True)
    return data        



def plot_line(data,image_path):
    
            # Plotting a simple line graph
    # Assuming you have a column named 'temperature' in your DataFrame for the y-axis data
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.plot(data.index, data['temperature'], marker='o', linestyle='-')

    # Set labels and title
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Temperature Trend')

    # Show the plot
    plt.grid(True)
    plt.tight_layout()
    
    plt.savefig(image_path)
    plt.close()  # Close the plot to free up memory
    return image_path



def plot_scatter(data,image_path):
    
            # Plotting a simple line graph
    # Assuming you have a column named 'temperature' in your DataFrame for the y-axis data
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.scatter(data['temperature'], data['people_counter'], color='red', marker='o')
    plt.xlabel('Temperature')
    plt.ylabel('People Counter')
    plt.title('Temperature vs People Counter')
 
    # Show the plot
    plt.grid(True)
    plt.tight_layout()
    
    plt.savefig(image_path)
    plt.close()  # Close the plot to free up memory
    return image_path
        
def generate_report(data,report):
   
    data.drop(columns=['location'], inplace=True)
    # Separate the features and the target variable
    X = data.drop('temperature', axis=1)
   
    y = data['temperature']

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X, y)

        # Predictions
    predictions = model.predict(X)

    # Generate a report
    # Compute evaluation metrics
    mse = mean_squared_error(y, predictions)
    mae = mean_absolute_error(y, predictions)
    r_squared = r2_score(y, predictions)

    # Print the evaluation metrics
    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"R-squared: {r_squared}")
    

    # Explanation of predictions
    report += "Explanation of Predictions:\n"
    for i, pred in enumerate(predictions):
        report += f"Prediction {i+1}: The model predicted {pred} based on features {X.iloc[i]}\n"

    # Correlation analysis
    # For example, using coefficients for feature importance in a linear regression model
    report += "\nCorrelation and Insights:\n"
    report += "Feature Coefficients:\n"
    for i, coef in enumerate(model.coef_):
        report += f"Feature {X.columns[i]} has coefficient {coef}\n"

    # Recommendations and Solutions
    report += "\nRecommendations:\n"
    report += "Based on the analysis, consider modifying feature X to improve predictions.\n"
    
    # Add evaluation metrics (example: R-squared)
    r_squared = model.score(X, y)
    report += f"\nModel Evaluation:\nR-squared: {r_squared}\n"


    # Saving the report to a text file
    file_path = "report.txt"
    with open(file_path, "w") as file:
        file.write(report)

    return file_path  # Return the file path to the saved report






def check_threshold():
        # Define InfluxDB connection parameters
    token = "SckCRn0kqB-hwH4fmWtJvWOKihHLRWZo0zgsKoO71Yr7oURJENeqQCWcTlrVfkgqjWV1H6qku_WxdeTMwMcA9g=="
    org = "Temasek Polytechnic"
    url = "https://us-east-1-1.aws.cloud2.influxdata.com"
    database = "Smart Washroom"

    TOKEN="6710805577:AAHBPFVMpHi2WAa0NvglQcWP-sL6xjT_qK4"
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    variables = ["temperature","humidity","toilet_roll_usage","people_counter","light_intensity","soap_level","ammonia_level"]
    
    last_alert_time = {
    "temperature": 0,
    "humidity": 0,
    "toilet_roll_usage": 0,
    "people_counter": 0,
    "light_intensity": 0,
    "soap_level": 0,
    "ammonia_level": 0,
    # Add other variables here
}
    
    variable_thresholds = {
        "temperature": 30.0,
        "humidity": 40.0,
        "toilet_roll_usage": 60.0,
        "light_intensity" : 400,
        "people_counter": 50,
        "light_intensity": 500.0,
        "soap_level": 70.0,
        "ammonia_level": 0.02,
        # Add other variables and their thresholds here
    }
    
    consecutive_data = {
    "temperature": [],
    "humidity": [],
    "toilet_roll_usage": [],
    "people_counter": [],
    "light_intensity": [],
    "soap_level": [],
    "ammonia_level": [],
    # Add other variables here
}

    bot = Bot(token=TOKEN)

    while True:
       current_time = time.time()

       for variable, threshold in variable_thresholds.items():
            query = f'''
            from(bucket: "{database}")
              |> range(start: -5m)
              |> filter(fn: (r) => r._measurement == "environmental_data" and r._field == "{variable}" and r._value > {threshold} )
              |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
              |> sort(columns:["_time"], desc: true)
              
            '''

            # Query InfluxDB using the Flux query
            result = client.query_api().query_data_frame(org=org, query=query)
            print(result)
            if not result.empty:
               for index, row in result.iterrows():
                consecutive_data[variable].append(row[variable])
                if len(consecutive_data[variable]) > 5:
                    consecutive_data[variable].pop(0)

                # Check if the last five values are above 30
                if all(val > threshold for val in consecutive_data[variable]):
                    if (current_time - last_alert_time[variable]) > 300:  # Adjust 300 to the desired time interval in seconds
                        bot.send_message(chat_id="1554346308", text=f"{variable} threshold exceeded!")
                        last_alert_time[variable] = current_time  # Update the last alert time for this variable

            time.sleep(1)  # Wait for 1 second before checking the next variable

       time.sleep(60)  # Wait for 60 seconds before checking again

            
        
        
        

def main():
    updater = Updater(token="6710805577:AAHBPFVMpHi2WAa0NvglQcWP-sL6xjT_qK4", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start",start))
    
    dp.add_handler(CommandHandler("graph", reply))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    
    dp.add_handler(CommandHandler("report", replies))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, replies))
    
    dp.add_handler(CommandHandler("live", live))
    dp.add_handler(CommandHandler("static", static))
    #create_alert_tasks()
    
 
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.regex('^\d+$'), handle_report))
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.regex('^\d+$'), handle_graph))
    updater.start_polling()

    check_threshold()

if __name__ == '__main__':
    # schedule.every(10).minutes.do(check_threshold)
    main()
