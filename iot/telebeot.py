import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
bot = telebot.TeleBot('6809283875:AAEn-r_kthHS62fn6i46IX8vNgTBhQQrkeQ')

# Dictionary to store the status and cleanliness of toilets
toilet_status = {
    'toilet1': {'occupied': False, 'clean': False},
    'toilet2': {'occupied': False, 'clean': False},
    'toilet3': {'occupied': False, 'clean': False},
}

# Define a handler for the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    welcome_message = "Welcome, Janitor! 🧹\n\n"
    welcome_message += "Available commands:\n"
    welcome_message += "/check_toilets - Check toilets status\n"
    welcome_message += "/clean_toilet1 - Mark Toilet 1 as clean\n"
    welcome_message += "/occupy_toilet1 - Mark Toilet 1 as occupied\n"
    welcome_message += "/free_toilet1 - Mark Toilet 1 as free\n"
    bot.reply_to(message, welcome_message)

# Command to check toilets status
@bot.message_handler(commands=['check_toilets'])
def check_toilets(message):
    status_message = "Toilet Status:\n"
    for toilet, info in toilet_status.items():
        status_message += f"{toilet}: "
        if info['occupied']:
            status_message += "Occupied"
        else:
            status_message += "Free"
        if info['clean']:
            status_message += " (Clean)\n"
        else:
            status_message += " (Not Clean)\n"
    bot.reply_to(message, status_message)

# Command to mark Toilet 1 as clean
@bot.message_handler(commands=['clean_toilet1'])
def clean_toilet1(message):
    toilet_status['toilet1']['clean'] = True
    bot.reply_to(message, "Toilet 1 has been marked as clean.")

# Command to mark Toilet 1 as occupied
@bot.message_handler(commands=['occupy_toilet1'])
def occupy_toilet1(message):
    toilet_status['toilet1']['occupied'] = True
    bot.reply_to(message, "Toilet 1 has been marked as occupied.")

# Command to mark Toilet 1 as free
@bot.message_handler(commands=['free_toilet1'])
def free_toilet1(message):
    toilet_status['toilet1']['occupied'] = False
    bot.reply_to(message, "Toilet 1 has been marked as free.")

# Similarly, add handlers for managing Toilet 2 and Toilet 3

# Start the bot
bot.polling()
