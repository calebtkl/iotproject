from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters, CommandHandler
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import influxdb_client


# Simulated query function for testing
def queries(hours):
    token = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
    org = "Temasek Polytechnic"
    url = "https://us-east-1-1.aws.cloud2.influxdata.com"
    
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
     
    
    # Replace this with your actual data querying logic
    # Example data generation for demonstration purposes
    query = f"""
        from(bucket: "Smart Washroom")
        |> range(start: -{hours}h)
        |> filter(fn: (r) => r._measurement == "environmental_data" and (r.location == "location_A" or r.location == "location_B"))
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> sort(columns:["_time"], desc: true)
    """
    df = client.query_api().query_data_frame(org=org, query=query)
 
    return df

# Function to plot scatter graph
def plot_scatter_graph(df, x_var, y_var):
    x = df[x_var]
    y = df[y_var]

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, alpha=0.7)
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.title(f'{y_var} vs {x_var}')
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

# Function to plot line graph
def plot_line_graph(df, x_var, y_var):
    x = df[x_var]
    y = df[y_var]

    plt.figure(figsize=(8, 6))
    plt.plot(x, y)
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.title(f'{y_var} over {x_var}')
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

# Function to handle /start command
def start(update, context) -> None:
     user = update.message.from_user
    
    
     context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello, {user.first_name}!")

# Function to handle graph type selection, hours, and variable selection
def combined_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query:
        query.answer()

        try:
            if 'graph_type' not in context.user_data:
                # Initial graph type selection
                keyboard = [
                    [InlineKeyboardButton("Scatter Graph", callback_data='scatter')],
                    [InlineKeyboardButton("Line Graph", callback_data='line')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text('Please select a graph type:', reply_markup=reply_markup)

            elif 'hours' not in context.user_data:
                # Hours selection
                hours = int(query.message.text)
                context.user_data['hours'] = hours

                graph_type = query.data
                context.user_data['graph_type'] = graph_type

                keyboard = [
                    [InlineKeyboardButton(var, callback_data=var) for var in ['temperature', 'humidity', 'ammonia_level', 'cleanliness_score']],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text('Please select a variable to plot:', reply_markup=reply_markup)
            else:
                # Variable selection
                selected_variable = query.data
                hours = context.user_data['hours']

                df = queries(hours)
                scatter_buffer = plot_scatter_graph(df, 'ammonia_level', selected_variable)  # Adjust x_var and y_var as needed
                query.message.reply_photo(photo=scatter_buffer)

        except (ValueError, TypeError):
            query.message.reply_text("Please enter a valid number.")
# Function to initialize the bot
def main() -> None:
   
    
 
    updater = Updater("6847070025:AAFOuIl3agqB2bPYSzUJ9Q_r8ch5GrgdtQ0", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler('plot',combined_callback))
   

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
