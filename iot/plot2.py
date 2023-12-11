import matplotlib.pyplot as plt
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import influxdb_client 
from influxdb_client.client.write_api import SYNCHRONOUS
from io import BytesIO

# Replace with your InfluxDB credentials
token = "6847070025:AAFOuIl3agqB2bPYSzUJ9Q_r8ch5GrgdtQ0"
# Define InfluxDB connection parameters
token1 = "KXMpn2P9uje6hQ6MQFuumGz19EYsxcU2FLkSnyBb5q2hN_h5plIoQSFF1_9rbJKgatw6fcBoc7fLysZPbmfiiw=="
org = "Temasek Polytechnic"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "Smart Washroom"

# Create an InfluxDB client object
client = influxdb_client.InfluxDBClient(url=url, token=token1, org=org)

# Create an InfluxDB client object
client = influxdb_client.InfluxDBClient(url=url, token=token1, org=org)

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
        update.callback_query.reply_text("Please provide at least two variable header names.")
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
    try:
        hours = int(update.message.text)
        if hours <= 0:
            raise ValueError("Please enter a positive integer for hours.")
        
        keyboard = [
            [InlineKeyboardButton("Scatter Graph", callback_data='scatter')],
            [InlineKeyboardButton("Line Graph", callback_data='line')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Choose a graph type:", reply_markup=reply_markup)
        context.user_data['hours'] = hours
    except ValueError as e:
        update.message.reply_text(str(e))

# Handler to handle graph type selection
def select_graph_type(update, context):
    query = update.callback_query
    graph_type = query.data
    query.answer()
  
    context.user_data['graph_type'] = graph_type
    print(graph_type)
    
    if graph_type in ['scatter', 'line']:
        query.edit_message_text(text=f"Selected: {graph_type.capitalize()}")
        context.user_data['graph_type'] = graph_type
        if graph_type == 'scatter':
            select_x_variable(update, context)  # Initiate x variable selection for scatter
        elif graph_type == 'line':
            select_x_variable(update, context)  # Initiate y variable selection for line
    else:
        query.edit_message_text(text="Invalid graph type selection")
        
    return
    
    
    

# Handler to handle x variable selection
def select_x_variable(update, context):
    # Create an inline keyboard for selecting the x variable
    keyboard = [
        [
            InlineKeyboardButton("Temperature", callback_data="x_temperature"),
            InlineKeyboardButton("Humidity", callback_data="x_humidity"),
            # Add more buttons for x variables as needed
        ],
        [
            InlineKeyboardButton("Done", callback_data="x_done_selection")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Select X variable:", reply_markup=reply_markup)
    return

# Handler to handle y variable selection
def select_y_variable(update, context):
    # Create an inline keyboard for selecting the y variable
    keyboard = [
        [
            InlineKeyboardButton("Temperature", callback_data="y_temperature"),
            InlineKeyboardButton("Humidity", callback_data="y_humidity"),
            # Add more buttons for y variables as needed
        ],
        [
            InlineKeyboardButton("Done", callback_data="y_done_selection")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Select Y variable:", reply_markup=reply_markup)

# Handler to handle callback queries for x and y variables
def callback_handler(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    
    # Handle x variable selection
    if data.startswith("x_"):
        selected_x_variable = data.split("_", 1)[1]
        query.edit_message_text(text=f"X Variable Selected: {selected_x_variable}")
    
    # Handle y variable selection
    elif data.startswith("y_"):
        selected_y_variable = data.split("_", 1)[1]
        query.edit_message_text(text=f"Y Variable Selected: {selected_y_variable}")
    
    # Handle 'Done' button for x variables
    elif data == "x_done_selection":
        select_y_variable(update, context)  # Move to selecting y variables
        
    # Handle 'Done' button for y variables
    elif data == "y_done_selection":
        query.edit_message_text(text="Selection complete!")
        # Perform any final actions or calculations using selected x and y variables
        
    else:
        query.edit_message_text(text="Invalid selection")

# Command handler to start the bot
def start(update, context):
    update.message.reply_text("Welcome to the Graph Bot! Please /sethours to choose the hours.")

# Error handler
def error(update, context):
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
    dispatcher.add_handler(CallbackQueryHandler(select_x_variable, pattern='^x_'))
    dispatcher.add_handler(CallbackQueryHandler(select_y_variable, pattern='^y_'))
    dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
