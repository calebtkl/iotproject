from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters, CommandHandler
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import influxdb_client

# Replace with your InfluxDB credentials
token = "6847070025:AAFOuIl3agqB2bPYSzUJ9Q_r8ch5GrgdtQ0"
token1 = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
org = "Temasek Polytechnic"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

# Initialize InfluxDB client
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

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

# Function to plot graph
def plot_graph(update, context, hours, graph_type):
    query = f"""
        from(bucket: "Smart Washroom")
        |> range(start: -{hours}h)
        |> filter(fn: (r) => r._measurement == "environmental_data" and (r.location == "location_A" or r.location == "location_B"))
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> sort(columns:["_time"], desc: true)
    """
    df = client.query_api().query_data_frame(org=org, query=query)

    variable_names = context.user_data.get('variable_names', [])
    if len(variable_names) < 2:
        update.message.reply_text("Please provide at least two variable header names.")
        return

    x_var, y_var = variable_names[:2]

    if graph_type == 'scatter':
        buffer = plot_scatter_graph(df, x_var, y_var)
    elif graph_type == 'line':
        buffer = plot_line_graph(df, x_var, y_var)
    else:
        update.message.reply_text("Invalid graph type selected.")
        return

    # Send the image to the Telegram chat
    update.message.reply_photo(photo=buffer)

# Command handler to start the bot
def start(update, context):
    update.message.reply_text("Welcome to the Graph Bot! Please /sethours to choose the hours.")

# Handler to set hours
def set_hours(update, context):
    update.message.reply_text("Please enter the number of hours:")

# Handler to handle the user input for hours
def get_hours(update, context):
    hours = int(update.message.text)
    keyboard = [
        [InlineKeyboardButton("Scatter Graph", callback_data='scatter')],
        [InlineKeyboardButton("Line Graph", callback_data='line')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose a graph type:", reply_markup=reply_markup)
    context.user_data['hours'] = hours

# Handler to handle graph type selection
def select_graph_type(update, context):
    query = update.callback_query
    graph_type = query.data
    query.answer()
    query.edit_message_text(text=f"Selected: {graph_type.capitalize()}")
    context.user_data['graph_type'] = graph_type
    query.message.reply_text("Enter variable header names separated by commas:")

# Handler to handle variable header names input
def get_variable_names(update, context):
    if update.message is None:
        return  # Exit if there's no message in the update

    variable_names = update.message.text.split(',')
    context.user_data['variable_names'] = variable_names

    # Ensure there's a chat context before replying
    if context.chat_data is None:
        return

    # Call the plot_graph function with the gathered data
    plot_graph(update, context, context.user_data.get('hours'), context.user_data.get('graph_type'))

# Error handler
def error(update, context):
    """Log Errors caused by Updates."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {context.error}")

# Main function
def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('sethours', set_hours))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_hours))
    dispatcher.add_handler(CallbackQueryHandler(select_graph_type))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_variable_names))
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
