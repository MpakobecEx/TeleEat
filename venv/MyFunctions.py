import telebot
from SQL import *
from strings import *


def GetHelpMessageOld():
    return MESSAGE_HELP

def GetHelpMessageOld():
    f = open('texts/help.txt', 'r')
    mes = f.read()
    f.close()
    return str(mes).encode('cp1251')


def GetOrderCompleteMessange():
    otv = GetShopInfo(GetOrderInfo(GetOpenOrderID())[1])
    mes = "Для заказа используте:\nСайт: " + otv[2] + "\n"
    mes = mes + "Телефон: " + otv[1] + "\n\n"
    mes += "/order_look_all - просмотр всего заказа.\n"
    mes += "/order_end - заказ привезли, закрываем."
    return mes


def GetPositionsMessange(order_id):
    mes = "Общий заказ на сумму " + str(GetSumma(order_id)) + "руб.\n\n"
    ords = GetPositionsList()
    for ord in ords:
        mes = mes + str(ord[0]) + " [x" + str(ord[1]) + "] = " + str(ord[2]) + "руб.\n"
    return mes


def GetPositionsMessangeForUser(order_id, id):
    mes = "Ваш личный заказ на сумму " + str(GetSummaForUser(order_id, id)) + "руб.\n\n"
    ords = GetPositionsListForUser(order_id, id)
    for ord in ords:
        mes = mes + str(ord[0]) + " [x" + str(ord[1]) + "] = " + str(ord[2]) + "руб.\n"
    return mes


def GetPositionsMessangeDetail(order_id):
    mes = "Детальный заказ на сумму " + str(GetSumma(GetOpenOrderID())) + "руб.\n\n"
    users = GetUserList()
    for user in users:
        poss = GetPositionsListForUser(order_id, user)
        if len(poss) != 0:
            mes += GetUserInfo(user)[0] + " на сумму " + str(GetSummaForUser(order_id, user)) + ":\n"
            for pos in poss:
                mes += pos[0] + "[x" + str(pos[1]) + "] - " + str(pos[2]) + "\n"
            mes += "\n"

    return mes


def GetKeyboardOtmena():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Отмена')
    return keyboard


def GetMessageStartOrderForUsers():
    shop_id = GetOrderInfo(GetOpenOrderID())[1]
    otv = GetShopInfo(shop_id)
    name = GetUserInfo(GetOrderInfo(GetOpenOrderID())[0])[0]
    mes = "Господин " + name + " соизволил сделать заказ!\nЗаведение: " + otv[0] + "\nСайт: " + otv[2]
    return mes


def GetMessageStartOrderForMain():
    shop_id = GetOrderInfo(GetOpenOrderID())[1]
    otv = GetShopInfo(shop_id)
    mes = "Вы соизволили сделать заказ!\nЗаведение: " + otv[0] + "\nТелефон: " + otv[1] + "\nСайт: " + otv[2]
    return mes

def GetShopsMarkup():
    markup = telebot.types.InlineKeyboardMarkup()
    for shop in GetShopsList():
        markup.add(telebot.types.InlineKeyboardButton(text=shop[1], callback_data=int(shop[0])))
    markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data=999))
    return markup


def GetMenuMarkup(parent):
    markup = telebot.types.InlineKeyboardMarkup()
    shops = GetShopsList()
    order_id = GetOpenOrderID()
    shop_id = GetOrderInfo(order_id)[1]
    for menu in GetMenu(shop_id, parent):
        name = menu[1]
        if parent != 0:
            name += " - " + str(menu[2]) + "руб"
        markup.add(telebot.types.InlineKeyboardButton(text=name, callback_data=int(menu[0])))
    if parent != 0:
        markup.add(telebot.types.InlineKeyboardButton(text='<<<Назад', callback_data=999))
    return markup