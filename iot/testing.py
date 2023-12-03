from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import filters


import pyqrcode

kaninabu = Bot(token='6701891410:AAFK_T8SB3j0gloQ1X4ouk2hYltpmdKOPEY')
kaninabu = Dispatcher


# ...

@kaninabu.message_handler(filters.Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Click Me")
    keyboard.add(item)
    await message.answer("Welcome to your Telegram bot! Send me any message, and I'll respond.", reply_markup=keyboard)

@kaninabu.message_handler(filters.Text)
async def echo(message: types.Message):
    await message.answer(f"You said: {message.text}")