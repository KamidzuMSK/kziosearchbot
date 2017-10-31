# -*- coding: utf-8 -*-

import telebot
import config
import requests
import datetime
from telebot import types


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"]) # Обработка /start
def handle_start(message):
        now = datetime.datetime.now()
        today = now.day
        hour = now.hour
        if today == now.day and 6 <= hour < 12:
                bot.send_message(message.from_user.id, 'Доброе утро!')
                today += 1
        elif today == now.day and 12 <= hour < 17:
                bot.send_message(message.from_user.id, 'Добрый день!')
                today += 1
        elif today == now.day and 17 <= hour < 23:
                bot.send_message(message.from_user.id, 'Добрый вечер!')
                today += 1
        kb = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
        kb.add('Тестовый режим','Начать работу')
        msg = bot.send_message(message.chat.id, 'Пожалуйста, выберите режим работы.', reply_markup=kb)
        bot.register_next_step_handler(msg, process_search_parameters_select)
        
def process_search_parameters_select(message):
        hide_markup = telebot.types.ReplyKeyboardRemove()
        if message.text.encode('utf-8')=='Тестовый режим':
           r = requests.get('http://map.kzn.ru/saumi_auction_xml/au_objects.json')
           data = r.json()
           date = data["data"][0]["AU_DATE"]
           time = data["data"][0]["AU_TIME"]
           objtype = data["data"][0]["OBJECT_TYPE_NAME"]
           autype = data["data"][0]["AUCTION_TYPE_NAME"]
           rmplan = data["data"][0]["AU_RMPLAN"]
           townarea = data["data"][0]["TOWNAREA"]
           address = data["data"][0]["ADDRESS"]
           kadastrno = data["data"][0]["KADASTRNO"]
           srok = data["data"][0]["AU_SROK"]
           square = data["data"][0]["SQUARE"]
           stprice = data["data"][0]["AU_STARTPRICE"]
           target = data["data"][0]["AU_TARGET"]
           aulink = data["data"][0]["AU_LINKS"]
           keyboard = types.InlineKeyboardMarkup()
           map_button = types.InlineKeyboardButton(text="Показать на карте", url="https://yandex.ru/maps/43/kazan/?mode=search&text={}".format(address.encode('utf-8').replace(' ', '')))
           url_button = types.InlineKeyboardButton(text="Посмотреть объявление", url="{}".format(aulink))
           if aulink != '':
                   keyboard.add(url_button)
           if address != '':
                   keyboard.add(map_button) 
           bot.send_message(message.chat.id, "Бот переключён в режим тестирования!\nПример вывода сведений об объекте.", reply_markup=hide_markup)
           bot.send_message(message.chat.id, "Дата и время аукциона: {} {}\nВид объекта: {}\nУсловия продажи: {}\nМестоположение объекта: {}\n\
Координаты объекта: \nрайон: {}, адрес: {}\nКадастровый номер: {}\nСрок аренды: {} мес. Площадь: {} кв. м.\nСтартовая цена: {} руб.\nЦелевое назначение: {}\n\
".format(date, time, objtype.encode('utf-8'), autype.encode('utf-8'), rmplan.encode('utf-8'), townarea.encode('utf-8'), address.encode('utf-8'), kadastrno, srok, square, stprice, target.encode('utf-8')), reply_markup=keyboard)
        elif message.text.encode('utf-8')=='Начать работу':
           bot.send_message(message.chat.id, "Бот находится в стадии разработки или отладки. Попробуйте, пожалуйста, позднее.", reply_markup=hide_markup)    
##           kbd = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
##           kbd.add('Дата торгов','Время торгов', 'Вид объекта', 'Условия продажи', 'Местоположение', 'Район', 'Адрес', 'Кадастровый №', 'Срок аренды', 'Общая площадь', 'Стартовая цена')
##           msg = bot.send_message(message.chat.id, 'Пожалуйста, выберите параметр для поиска.', reply_markup=kbd)
##           bot.register_next_step_handler(msg, process_search)
##
##def process_search(message):
##        if message.text.encode('utf-8')=='Дата торгов':
##           r = requests.get('http://map.kzn.ru/saumi_auction_xml/au_objects.json')
##           data = r.json()
##           for index in range(len(data["data"])): 
##              print data["data"][index]["AU_DATE"]
##        if message.text.encode('utf-8')=='Время торгов':
##
##        if message.text.encode('utf-8')=='Вид объекта':
##
##        if message.text.encode('utf-8')=='Условия продажи':
##
##        if message.text.encode('utf-8')=='Местоположение':
##
##        if message.text.encode('utf-8')=='Район':
##
##        if message.text.encode('utf-8')=='Адрес':
##
##        if message.text.encode('utf-8')=='Кадастровый №':
##
##        if message.text.encode('utf-8')=='Срок аренды':
##
##        if message.text.encode('utf-8')=='Общая площадь':
##
##        if message.text.encode('utf-8')=='Стартовая цена':


if __name__ == '__main__':
    bot.polling(none_stop=True)
