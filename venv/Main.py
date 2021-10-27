import telebot
import config
from SQL import *
from MyFunctions import *
from strings import *

bot = telebot.TeleBot(config.TOKEN)

message_ids = {}


@bot.message_handler(commands=['start'])
def command_start(message):
    id = message.from_user.id
    if not CheckUser(id):
        CreateUser(id)
        bot.send_message(id, "Укажите имя для отображения остальным участникам.\nХотя бы фамилию...")
    else:
        bot.send_message(id, "Вы уже зарегистрированы, Василий!")


@bot.message_handler(commands=['help'])
def command_help(message):
    id = message.from_user.id
    #bot.send_message(id, GetHelpMessage())
    print("Nya")
    #bot.send_message(id, MESSAGE_HELP)


@bot.message_handler(commands=['info_name_edit'])
def command_change_name(message):
    id = message.from_user.id
    if not CheckStatus(id, 0):
        bot.send_message(id, MESSAGE_CANT_EDIT)
        return
    ChangeUserStatus(id, -5)
    bot.send_message(id, "Ожидание нового имени.\n" + MESSAGE_OTMENA, reply_markup=GetKeyboardOtmena())


@bot.message_handler(commands=['info_phone_edit'])
def command_change_phone(message):
    id = message.from_user.id
    if not CheckStatus(id, 0):
        bot.send_message(id, MESSAGE_CANT_EDIT)
        return
    ChangeUserStatus(id, -4)
    bot.send_message(id, "Ожидание нового телефона.\n" + MESSAGE_OTMENA, reply_markup=GetKeyboardOtmena())


@bot.message_handler(commands=['order_new'])
def send_order_new(message):
    id = message.from_user.id
    if CheckOpenOrder():
        bot.send_message(id, "Заказ делает кто-то другой :с")
    else:
        res = bot.send_message(id, "Выберите заведение для заказа.", reply_markup=GetShopsMarkup())
        message_ids[id] = res.message_id
        ChangeUserStatus(id, 1)


@bot.message_handler(commands=['order_complete'])
def send_order_close(message):
    id = message.from_user.id
    if not CheckOpenOrder():
        bot.send_message(id, MESSAGE_ORDER_NOTCREATE)
        return
    if GetOrderInfo(GetOpenOrderID())[0] != id:
        bot.send_message(id, "Не ты его породил, не ты его и закроешь...")
        return
    DeleteOrderTailAllNULL()
    bot.send_message(id, GetOrderCompleteMessange())
    otv = GetUserInfo(id)
    mes = "Этап сбора завершен.\nОтветственный делает заказ.\nДенежку сюда: " + otv[1] + "\n"
    mes += "/order_look - просмотр своего заказа.\n"
    mes += "/order_look_all - просмотр общего заказа."
    for user_id in message_ids.keys():
        bot.edit_message_reply_markup(user_id, message_ids[user_id])
    message_ids.clear()
    for user_id in GetAllUserList():
        ChangeUserStatus(user_id, 4)
        if user_id != id:
            otv = GetUserInfo(id)
            bot.send_message(user_id, mes)


@bot.message_handler(commands=['order_end'])
def send_order_complete(message):
    id = message.from_user.id
    if not CheckOpenOrder():
        bot.send_message(id, MESSAGE_ORDER_NOTCREATE)
        return
    if GetOrderInfo(GetOpenOrderID())[0] != id:
        bot.send_message(id, "Не ты его породил, не ты его и завершишь...")
        return
    SetOrderStop(GetOpenOrderID())
    ChangeUserStatus(id, 0)
    bot.send_message(id, "Спасибо за использование данного бота!")
    for user_id in GetAllUserList():
        ChangeUserStatus(user_id, 0)
        if user_id != id:
            bot.send_message(user_id, "Заказ приехал, побежали кушац!")


@bot.message_handler(commands=['order_cancel'])
def send_order_cancel(message):
    id = message.from_user.id
    if not CheckOpenOrder():
        bot.send_message(id, MESSAGE_ORDER_NOTCREATE)
        return
    if GetOrderInfo(GetOpenOrderID())[0] != id:
        bot.send_message(id, "Не ты его породил, не ты его и отменишь...")
        return
    DeleteOrderTailAllNULL()
    SetOrderStop(GetOpenOrderID())
    bot.send_message(id, "Жаль, очень жаль... Или ты всего лишь хочешь сменить заведение?")
    for user_id in message_ids.keys():
        bot.edit_message_reply_markup(user_id, message_ids[user_id])
    message_ids.clear()
    for user_id in GetAllUserList():
        ChangeUserStatus(user_id, 0)
        if user_id != id:
            bot.send_message(user_id, "Текущий заказ отменили :с")


@bot.message_handler(commands=['order_confirm'])
def send_order_confirm(message):
    id = message.from_user.id
    if not CheckOpenOrder():
        bot.send_message(id, MESSAGE_ORDER_NOTCREATE)
        return
    if CheckStatus(id, 2):
        bot.send_message(id, "Вы подтвердили заказ! \n/order_change - вернуться к редактирвоанию.")
        user_id = GetOrderInfo(GetOpenOrderID())[0]
        bot.send_message(user_id, "Господин " + GetUserInfo(id)[0] + " сделал заказ!")
        ChangeUserStatus(id, 4)
    else:
        bot.send_message(id, MESSAGE_WRONG)


@bot.message_handler(commands=['order_change'])
def send_order_change(message):
    id = message.from_user.id
    if not CheckOpenOrder():
        bot.send_message(id, MESSAGE_ORDER_NOTCREATE)
        return
    if CheckStatus(id, 4):
        ChangeUserStatus(id, 2)
        user_id = GetOrderInfo(GetOpenOrderID())[0]
        bot.send_message(user_id, "Господин " + GetUserInfo(id)[0] + " редактирует заказ!")
        res = bot.send_message(id, "Меню данного заведения:", reply_markup=GetMenuMarkup(0))
        message_ids[id] = res.message_id
    else:
        bot.send_message(id, MESSAGE_WRONG)


@bot.message_handler(commands=['order_look'])
def send_order_look(message):
    id = message.from_user.id
    if not CheckOpenOrder():
        bot.send_message(id, MESSAGE_ORDER_NOTCREATE)
        return
    if CheckStatus(id, 2) or CheckStatus(id, 3) or CheckStatus(id, 4):
        bot.send_message(id, GetPositionsMessangeForUser(GetOpenOrderID(), id))
    else:
        bot.send_message(id, MESSAGE_WRONG)


@bot.message_handler(commands=['order_look_detail'])
def send_order_look(message):
    id = message.from_user.id
    if not CheckOpenOrder():
        bot.send_message(id, MESSAGE_ORDER_NOTCREATE)
        return
    if CheckStatus(id, 2) or CheckStatus(id, 3) or CheckStatus(id, 4):
        bot.send_message(id, GetPositionsMessangeDetail(GetOpenOrderID()))
    else:
        bot.send_message(id, MESSAGE_WRONG)


@bot.message_handler(commands=['order_look_all'])
def send_order_look_all(message):
    id = message.from_user.id
    if not CheckOpenOrder():
        bot.send_message(id, MESSAGE_ORDER_NOTCREATE)
        return
    if CheckStatus(id, 2) or CheckStatus(id, 3) or CheckStatus(id, 4):
        bot.send_message(id, GetPositionsMessange(GetOpenOrderID()))
    else:
        bot.send_message(id, MESSAGE_WRONG)


@bot.message_handler(commands=['order_clear'])
def send_order_clear(message):
    id = message.from_user.id
    if not CheckOpenOrder():
        bot.send_message(id, MESSAGE_ORDER_NOTCREATE)
        return
    if CheckStatus(id, 2) or CheckStatus(id, 3) or CheckStatus(id, 4):
        DeleteOrderTailForUser(id)
        bot.send_message(id, "Ваш список заказа очищен.")
    else:
        bot.send_message(id, MESSAGE_WRONG)


@bot.message_handler()
def send_something(message):
    id = message.from_user.id
    #Редактирование имени
    if CheckStatus(id, -5):
        ChangeUserStatus(id, 0)
        if message.text == "Отмена":
            bot.send_message(id, MESSAGE_EDITCANCEL, reply_markup=telebot.types.ReplyKeyboardRemove())
            return
        ChangeNameUser(id, message.text)
        bot.send_message(id, "Имя успешно изменено.", reply_markup=telebot.types.ReplyKeyboardRemove())
    #Редактирование телефона
    elif CheckStatus(id, -4):
        ChangeUserStatus(id, 0)
        if (message.text == "Отмена"):
            bot.send_message(id, MESSAGE_EDITCANCEL, reply_markup=telebot.types.ReplyKeyboardRemove())
            return
        ChangePhoneUser(id, message.text)
        bot.send_message(id, "Телефон успешно изменен.", reply_markup=telebot.types.ReplyKeyboardRemove())
    #Имя для нового юзера
    elif CheckStatus(id, -2):
        ChangeNameUser(id, message.text)
        ChangeUserStatus(id, -1)
        bot.send_message(id, "А номер телефона для сбора баблища?")
    #Телефон для нового юзера
    elif CheckStatus(id, -1):
        ChangePhoneUser(id, message.text)
        ChangeUserStatus(id, 0)
        bot.send_message(id, "Регистрация завершена.")
        bot.send_message(id, GetHelpMessage())
    #Указываем количество
    elif CheckStatus(id, 3):
        if (message.text == "0"):
            DeleteOrderTailNULL(id)
            bot.send_message(id, "Позиция удалена.")
            res = bot.send_message(id, "Меню данного заведения:", reply_markup=GetMenuMarkup(0))
            message_ids[user_id] = res.message_id
        else:
            if (not str.isdigit(message.text)):
                bot.send_message(id, MESSAGE_WRONG)
                return
            count = int(message.text)
            if (count < 0):
                bot.send_message(id, MESSAGE_WRONG)
                return
            UpdateOrderTailNULL(id, count)
            bot.send_message(id, "Позиция успешно добавлена/изменена. Изволите ли что еще?")
            res = bot.send_message(id, "Меню данного заведения:", reply_markup=GetMenuMarkup(0))
            message_ids[id] = res.message_id
        ChangeUserStatus(id, 2)
    else:
        bot.send_message(id, "Ты сейчас договоришься...")


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    id = call.message.chat.id
    num = int(call.data)
    if CheckStatus(id, 1):
        if num == 999:
            bot.send_message(id, MESSAGE_ORDERCANCEL)
            bot.edit_message_reply_markup(id, call.message.message_id)
        elif num in (2, 3):
            bot.send_message(id, "Заведение в данный момент неактивно.\nВыберите другое.")
        else:
            bot.edit_message_reply_markup(id, call.message.message_id)
            CreateOrder(id, num)
            bot.send_message(id, GetMessageStartOrderForMain())
            for user_id in GetUserList():
                if user_id != id:
                    bot.send_message(user_id, GetMessageStartOrderForUsers())
                ChangeUserStatus(user_id, 2)
                res = bot.send_message(user_id, "Меню данного заведения:", reply_markup=GetMenuMarkup(0))
                message_ids[user_id] = res.message_id
    else:
        if num == 999:
            res = bot.edit_message_reply_markup(id, call.message.message_id, reply_markup=GetMenuMarkup(0))
            message_ids[id] = res.message_id
        else:
            shop_id = GetOrderInfo(GetOpenOrderID())[1]
            if CheckParent(shop_id, num):
                res = bot.edit_message_reply_markup(id, call.message.message_id, reply_markup=GetMenuMarkup(num))
                message_ids[id] = res.message_id
            else:
                res = bot.edit_message_reply_markup(id, call.message.message_id)
                message_ids[id] = res.message_id
                CreateOrderTail(id, num)
                ChangeUserStatus(id, 3)
                shop_id = GetOrderInfo(GetOpenOrderID())[1]
                position = GetPositionInfo(shop_id, num)
                bot.send_message(id, "Ваш выбор: " + position[0] + " - " + str(position[1]) + "\nУкажите количество.\nДля удаления позиции укажите 0.")

bot.infinity_polling()
