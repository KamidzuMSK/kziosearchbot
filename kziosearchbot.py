# -*- coding: utf-8 -*-

import telebot
import config
import requests


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"]) # Обработка /start
def handle_start(message):
    bot.send_message(message.from_user.id, 'Hi! \nMy friend')

@bot.message_handler(content_types=["text"])
def handle_t(message):
    if message.text[:7] == "Погода " or message.text[:7] == "погода " :
            city = message.text[7:]
            r = requests.get('http://api.openweathermap.org/data/2.5/weather?&units=metric&q=%s&appid=0c9f3c052f1d81b7062750ff0926f345<img src="https://habrastorage.org/files/8fa/5f5/313/8fa5f5313b37438eb250b22cf041f2dd.png" alt="image"/>' % (city))
            data = r.json()
            temp = data["main"]["temp"]
            bot.send_message(message.chat.id, 'Температура в ', city, ': ',temp , '°C')

bot.polling(none_stop=True, interval=0)
