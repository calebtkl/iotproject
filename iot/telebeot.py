import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
bot = telebot.TeleBot('6809283875:AAEn-r_kthHS62fn6i46IX8vNgTBhQQrkeQ')

# Dictionary to store the status and cleanliness of toilets
toilet_status = {
    'toilet1': {'occupied': False, 'clean': False},
    'toilet2': {'occupied': False, 'clean': False},
    'toilet3': {'occupied': False, 'clean': False},
}
cleaners = {}  # Dictionary to store cleaner information
# Define a handler for the '/start' command

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    welcome_message = "Welcome to the Toilet Management Bot! 🧼🚽\n\n"
    welcome_message += "Use the following commands:\n"
    welcome_message += "/check_toilets - Check toilets status\n"
    welcome_message += "/clean_toilet1 - Mark Toilet 1 as clean\n"
    welcome_message += "/occupy_toilet1 - Mark Toilet 1 as occupied\n"
    welcome_message += "/free_toilet1 - Mark Toilet 1 as free\n"
    welcome_message += "/cleaner - Register as a cleaner\n"
    welcome_message += "/status - Check your cleaning availability\n"
    welcome_message += "/absent - Mark yourself as absent\n"
    welcome_message += "/present - Mark yourself as present\n"
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



@bot.message_handler(commands=['cleaner'])
def cleaner_command(message):
    user_id = message.from_user.id
    if user_id not in cleaners:
        cleaners[user_id] = {'available': True}  # New cleaner added by default as available
        bot.reply_to(message, "You've been added as a cleaner.")
    else:
        bot.reply_to(message, "You are already registered as a cleaner.")


@bot.message_handler(commands=['status'])
def status_command(message):
    user_id = message.from_user.id
    if user_id in cleaners:
        if cleaners[user_id]['available']:
            bot.reply_to(message, "You are available for cleaning.")
        else:
            bot.reply_to(message, "You are currently unavailable for cleaning.")
    else:
        bot.reply_to(message, "You are not registered as a cleaner. Use /cleaner command to register.")


@bot.message_handler(commands=['absent'])
def absent_command(message):
    user_id = message.from_user.id
    if user_id in cleaners:
        cleaners[user_id]['available'] = False
        bot.reply_to(message, "You've been marked as absent.")
    else:
        bot.reply_to(message, "You are not registered as a cleaner. Use /cleaner command to register.")


@bot.message_handler(commands=['present'])
def present_command(message):
    user_id = message.from_user.id
    if user_id in cleaners:
        cleaners[user_id]['available'] = True
        bot.reply_to(message, "You've been marked as present and available for cleaning.")
    else:
        bot.reply_to(message, "You are not registered as a cleaner. Use /cleaner command to register.")


bot.polling()
