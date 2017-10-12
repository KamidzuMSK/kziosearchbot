# -*- coding: utf-8 -*-

import telebot

API_TOKEN = '423472303:AAFLD7h1pPYAYVqe6CauuOwcnkDwKzihnyM'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """
Привет! 
Я тестовый бот, и умею я пока немного. Напиши мне и я отвечу!
""")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.polling()
