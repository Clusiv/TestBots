import telebot
from config import tokens
bot = telebot.TeleBot(tokens['simpledialog']) 

users = {}
start = """
Hi. This is a simple bot that implement some dialog.
Code you can find on github:
github.com/clusiv/simpleBots/simpledialog.py

Now follow bot questions.
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    users[message.chat.id] = {}
    users[message.chat.id]['state'] = 0
    bot.reply_to(message, start)
    bot.send_message(message.chat.id, 'What is your name?')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if users[message.chat.id]['state'] == 0:
        users[message.chat.id]['state'] = 1
        users[message.chat.id]['name'] = message.text
        bot.send_message(message.chat.id, 'Where are you from?')

    elif users[message.chat.id]['state'] == 1:
        users[message.chat.id]['state'] = 2
        users[message.chat.id]['address'] = message.text
        bot.send_message(message.chat.id, 'What a fruit do you like?')

    elif users[message.chat.id]['state'] == 2:
        users[message.chat.id]['state'] = 3
        users[message.chat.id]['fruit'] = message.text
        # print(users[message.chat.id])
        output = ''.join([f'Your {key} : {value} \n' for key, value in users[message.chat.id].items()])
        bot.send_message(message.chat.id, output + '\nStart again /start')
        

bot.polling()