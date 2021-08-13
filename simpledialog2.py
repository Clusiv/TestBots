import telebot
from telebot import types
from config import tokens
bot = telebot.TeleBot(tokens['simpledialog2']) 

users = {}

start = """
Hi. This is a simple bot that implement some dialog.
Answering by buttons.
Code you can find on github:
https://github.com/Clusiv/TestBots/blob/master/simpledialog2.py

Now follow bot questions.
"""
markup_cities = types.InlineKeyboardMarkup()
city1 = types.InlineKeyboardButton('Malgobek', callback_data="address:Malgobek")
city2 = types.InlineKeyboardButton('Nazran', callback_data="address:Nazran")
city3 = types.InlineKeyboardButton('Karabulak', callback_data="address:Karabulak")
markup_cities.add(city1, city2, city3)

markup_fruits = types.InlineKeyboardMarkup()
fruit1 = types.InlineKeyboardButton('Banana', callback_data="fruit:Banana")
fruit2 = types.InlineKeyboardButton('Orange', callback_data="fruit:Orange")
fruit3 = types.InlineKeyboardButton('Apple', callback_data="fruit:Apple")
markup_fruits.add(fruit1, fruit2, fruit3)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    users[message.chat.id] = {}
    bot.reply_to(message, start)
    bot.send_message(message.chat.id, 'What is your name?')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    users[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, 'Where are you from?', reply_markup=markup_cities)

@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'address')
def callback_query(call):
    address = call.data.split(':')[1]
    users[call.message.chat.id]['address'] = address
    bot.answer_callback_query(call.id, f'Your address is ' + address)
    bot.send_message(call.message.chat.id, 'What a fruit do you like?', reply_markup=markup_fruits)

@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'fruit')
def callback_query(call):
    fruit = call.data.split(':')[1]
    users[call.message.chat.id]['fruit'] = fruit
    bot.answer_callback_query(call.id, f'Your fruit is ' + fruit)
    output = ''.join([f'Your {key} : {value} \n' for key, value in users[call.message.chat.id].items()])
    bot.send_message(call.message.chat.id, output + '\nStart again /start')

bot.polling()