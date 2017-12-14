# -*- coding: utf-8 -*-

import telebot
import config
import requests
import datetime
from telebot import types
from telegramcalendar import create_calendar
import os
from flask import Flask, request

bot = telebot.TeleBot(config.token)
server = Flask(__name__)
r = requests.get('http://map.kzn.ru/saumi_auction_xml/au_objects.json')
data = r.json()
main_menu_kb = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
main_menu_kb.add('Дата торгов','Время торгов', 'Вид объекта', 'Условия продажи', 'Местоположение', 'Район', 'Адрес', 'Кадастровый №', 'Срок аренды', 'Общая площадь', 'Стартовая цена')
search_results_sub_menu_kb = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
search_results_sub_menu_kb.add('В главное меню')
search_text=""

@bot.message_handler(commands=["start"])
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
        bot.send_message(message.chat.id, "Я помогу Вам в поиске информации по аукционам на недвижимость в Казани.")
        main_menu(message)

@bot.message_handler(commands=["main_menu"])
def handle_main_menu(message):
        main_menu(message)
        
def main_menu(message):        
        msg = bot.send_message(message.chat.id, 'Пожалуйста, выберите параметр для поиска.', reply_markup=main_menu_kb)
        bot.register_next_step_handler(msg, process_search_options)
        
def process_search_options(message):
        if message.text=='Дата торгов':
                process_audate_search_input(message)
        elif message.text=='Время торгов':
                process_autime_search_input(message)
        elif message.text=='Вид объекта':
                process_objtype_search_input(message)
        elif message.text=='Условия продажи':
                process_autype_search_input(message)
        elif message.text=='Местоположение':
                process_rmplan_search_input(message)
        elif message.text=='Район':
                process_townarea_search_input(message)
        elif message.text=='Адрес':
                process_address_search_input(message)
        elif message.text=='Кадастровый №':
                process_kadastrno_search_input(message)
        elif message.text=='Срок аренды':
                process_ausrok_search_input(message)
        elif message.text=='Общая площадь':
                process_square_search_input(message)
        elif message.text=='Стартовая цена':
                process_austartprice_search_input(message)
                
def process_audate_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите интересующую Вас дату аукциона")
        bot.register_next_step_handler(msg, process_audate_search)

def process_autime_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите интересующее Вас время аукциона")
        bot.register_next_step_handler(msg, process_autime_search)

def process_objtype_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите интересующий Вас вид объекта")
        bot.register_next_step_handler(msg, process_objtype_search)

def process_autype_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите интересующие Вас условия продажи объекта")
        bot.register_next_step_handler(msg, process_autype_search)

def process_rmplan_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите интересующее Вас местоположение объекта")
        bot.register_next_step_handler(msg, process_rmplan_search)

def process_townarea_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите интересующий Вас район")
        bot.register_next_step_handler(msg, process_townarea_search)

def process_address_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите интересующий Вас адрес")
        bot.register_next_step_handler(msg, process_address_search)

def process_kadastrno_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите кадастровый номер объекта")
        bot.register_next_step_handler(msg, process_kadastrno_search)

def process_ausrok_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите срок аренды")
        bot.register_next_step_handler(msg, process_ausrok_search)

def process_square_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите интересующую Вас общую площадь объекта")
        bot.register_next_step_handler(msg, process_square_search)

def process_austartprice_search_input(message):
        msg = bot.send_message(message.chat.id, "Укажите интересующую Вас стартовую цену объекта")
        bot.register_next_step_handler(msg, process_austartprice_search)

def process_audate_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["AU_DATE"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

def process_autime_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["AU_TIME"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

def process_objtype_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["OBJECT_TYPE_NAME"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

def process_autype_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["AUCTION_TYPE_NAME"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

def process_rmplan_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["AU_RMPLAN"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

def process_townarea_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["TOWNAREA"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

def process_address_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["ADDRESS"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

def process_kadastrno_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["KADASTRNO"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

def process_ausrok_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["AU_SROK"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")   

def process_square_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["SQUARE"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

def process_austartprice_search(message):
        results = 0
        search_text=message.text
        for index in range(len(data["data"])):
                if data["data"][index]["AU_STARTPRICE"].lower().find(search_text) != -1:
                        results += 1
                        search_results_inline_kb = types.InlineKeyboardMarkup()
                        search_results_inline_kb.add(*[types.InlineKeyboardButton(text="Подробнее об объекте", callback_data=index+1)])
                        bot.send_message(message.chat.id, "{}".format(data["data"][index]["ADDRESS"]), reply_markup = search_results_inline_kb)
        if results == 0:
                bot.send_message(message.chat.id, "По вашему запросу результатов не обнаружено")
        else:
                bot.send_message(message.chat.id, "По вашему запросу найдено результатов: {}".format(results))
        bot.send_message(message.chat.id, "Выберите один из результатов поиска и нажмите кнопку \"Подробнее об объекте\" под интересующим Вас адресом для вывода подробной информации.\nДля возврата в главное меню нажмите /main_menu")

@bot.callback_query_handler(func=lambda c:True)
def res_out(c):
        index=int(c.data)-1
        date = data["data"][index]["AU_DATE"]
        time = data["data"][index]["AU_TIME"]
        objtype = data["data"][index]["OBJECT_TYPE_NAME"]
        autype = data["data"][index]["AUCTION_TYPE_NAME"]
        rmplan = data["data"][index]["AU_RMPLAN"]
        townarea = data["data"][index]["TOWNAREA"]
        address = data["data"][index]["ADDRESS"]
        kadastrno = data["data"][index]["KADASTRNO"]
        srok = data["data"][index]["AU_SROK"]
        square = data["data"][index]["SQUARE"]
        stprice = data["data"][index]["AU_STARTPRICE"]
        target = data["data"][index]["AU_TARGET"]
        aulink = data["data"][index]["AU_LINKS"]
        keyboard = types.InlineKeyboardMarkup()
        map_button = types.InlineKeyboardButton(text="Примерное расположение", url="https://yandex.ru/maps/43/kazan/?mode=search&text={}".format(address.replace(' ', '')))
        url_button = types.InlineKeyboardButton(text="Посмотреть объявление", url="{}".format(aulink))
        if aulink != '':
                keyboard.add(url_button)
        if address != '':
                keyboard.add(map_button)
##        bot.send_message(с.message.chat.id, "Дата и время аукциона: {} {}\nВид объекта: {}\nУсловия продажи: {}\nМестоположение объекта: {}\nКоординаты объекта: \nрайон: {}, адрес: {}\n\
##Кадастровый номер: {}\nСрок аренды: {} мес. Площадь: {} кв. м.\nСтартовая цена: {} руб.\nЦелевое назначение: {}\n".format(date, time, objtype, autype, rmplan, townarea, address, kadastrno, srok, square, stprice, target), reply_markup=keyboard)
        msg = bot.edit_message_text(
                chat_id = c.message.chat.id,
                message_id = c.message.message_id,
                text = "Дата и время аукциона: {} {}\nВид объекта: {}\nУсловия продажи: {}\nМестоположение объекта: {}\nКоординаты объекта: \nрайон: {}, адрес: {}\n\
Кадастровый номер: {}\nСрок аренды: {} мес. Площадь: {} кв. м.\nСтартовая цена: {} руб.\nЦелевое назначение: {}\n".format(date, time, objtype, autype, rmplan, townarea, address, kadastrno, srok, square, stprice, target),
                parse_mode = "Markdown", reply_markup=keyboard)

##def res_list(c):
##        if c.data == 1:
##                bot.edit_message_text(
##                chat_id = c.message.chat.id,
##                message_id = c.message.message_id,
##                text = "Результаты поиска:",
##                parse_mode = "Markdown", reply_markup=search_results_inline_kb)
                
if __name__ == '__main__':
    bot.polling(none_stop=True)

@server.route("/423472303:AAFLD7h1pPYAYVqe6CauuOwcnkDwKzihnyM", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://powerfull-cliffs-51893/423472303:AAFLD7h1pPYAYVqe6CauuOwcnkDwKzihnyM")
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
