import telebot
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import uuid


# Replace "YOUR_BOT_TOKEN" with your actual bot's API token
bot = telebot.TeleBot("6559282439:AAHiZveMmc48Wl3uLSHpaD7d98Oig0LQjf4")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to your bot! Here are some available commands:\n"
                          "/help - Show this help message\n"
                          "/echo [text] - Echo back the provided text\n"
                          "/image - Send an image\n"
                          "/document - Send a document")

@bot.message_handler(commands=['echo'])
def echo_message(message):
    # Extract the text following the /echo command
    text_to_echo = message.text[6:]
    bot.reply_to(message, f"You said: {text_to_echo}")

@bot.message_handler(commands=['image'])
def send_image(message):
    # Send an image
    with open('屏幕截图 2023-10-24 191146.png', 'rb') as img:
        bot.send_photo(message.chat.id, img)

@bot.message_handler(commands=['document'])
def send_document(message):
    # Send a document (replace with an actual file path)
    with open('your_document.pdf', 'rb') as doc:
        bot.send_document(message.chat.id, doc)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "I don't understand that command. Type /help for a list of available commands.")

if __name__ == "__main__":
    bot.polling()
