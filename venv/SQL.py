import sqlite3

#Изменить имя юзеру
def ChangeNameUser(id, name):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/ChangeNameUser.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id, "name": name})
    con.commit()
    con.close()

#Изменить телефон юзеру
def ChangePhoneUser(id, phone):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/ChangePhoneUser.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id, "phone": phone})
    con.commit()
    con.close()

#Изменить статус юзеру
def ChangeUserStatus(id, status):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/ChangeStatusUser.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id, "status": status})
    con.commit()
    con.close()

#Проверка на открытый заказ
def CheckOpenOrder():
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/CheckOrders.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL)
    Count = cur.fetchone()[0]
    con.close()
    return Count == 1

#Проверка на наличие парента
def CheckParent(shop_id, parent):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/CheckParent.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"shop_id":shop_id, "parent": parent})
    otv = cur.fetchone()
    con.close()
    return otv[0] > 0

#Проверит статус юзера
def CheckStatus(id, status):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/CheckStatus.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id})
    Status = cur.fetchone()[0]
    con.close()
    return Status == status

#Проверка на существование юзера
def CheckUser(id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/CheckUser.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id})
    Count = cur.fetchone()[0]
    con.close()
    return Count > 0

#Создаст хеад заказа
def CreateOrder(id, shop):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/CreateOrder.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id, "shop": shop})
    con.commit()
    con.close()

#Создаст тейл заказа
def CreateOrderTail(user_id, position_id):
    DeleteOrderTail(user_id, position_id)
    order_id = GetOpenOrderID()
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/CreateOrderTail.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id": order_id, "user_id": user_id, "position_id": position_id})
    con.commit()
    con.close()

#Создаст юзера с айди
def CreateUser(id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/CreateUser.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id})
    con.commit()
    con.close()

#Удалит тейл заказа
def DeleteOrderTail(user_id, position_id):
    order_id = GetOpenOrderID()
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/DeleteOrderTail.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id": order_id, "user_id": user_id, "position_id": position_id})
    con.commit()
    con.close()

#Удалит все пустые тейлы активного заказа
def DeleteOrderTailAllNULL():
    order_id = GetOpenOrderID()
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/DeleteOrderTailAllNULL.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL)
    con.commit()
    con.close()

#Удалит все тейлы активного заказа юзера
def DeleteOrderTailForUser(user_id):
    order_id = GetOpenOrderID()
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/DeleteOrderTailForUser.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id": order_id, "user_id": user_id})
    con.commit()
    con.close()

#Удалит пустой тейл активного заказа юзера
def DeleteOrderTailNULL(user_id):
    order_id = GetOpenOrderID()
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/DeleteOrderTailNULL.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id": order_id, "user_id": user_id})
    con.commit()
    con.close()

#Вернет список id всех юзеров
def GetAllUserList():
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetAllUserList.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL)
    list = []
    ids = cur.fetchall()
    for id in ids:
        list.append(id[0])
    con.close()
    return list

#Вернет список id всех юзеров без определенного id
def GetAllUserListWithout(id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetAllUserListWithout.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id})
    list = []
    ids = cur.fetchall()
    for id in ids:
        list.append(id[0])
    con.close()
    return list

#Вернет максимальную позицию в заведении из активного заказа
def GetMaxPosition():
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetMaxPosition.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL)
    otv = cur.fetchone()
    con.close()
    return otv[0]

#Вернет меню для парента
def GetMenu(shop_id, parent):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetMenu.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"shop_id": shop_id, "parent": parent})
    list = []
    ords = cur.fetchall()
    for ord in ords:
        list.append([ord[0], ord[1], ord[2]])
    con.close()
    return list

#Вернет айди активного заказа
def GetOpenOrderID():
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetOpenOrderID.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL)
    otv = cur.fetchone()
    con.close()
    return otv[0]

#Вернет айди юзера из заказа
def GetUserFromOrder(id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetUserFromOrder.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id})
    otv = cur.fetchone()
    con.close()
    return otv[0]

#Вернет имя позиции с айди из заведения активного заказа
def GetPositionInfo(shop_id, id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetPositionInfo.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"shop_id": shop_id, "id": id})
    otv = cur.fetchone()
    con.close()
    return [otv[0], otv[1]]

#Вернет сообщение с общим заказом
def GetPositionsList():
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetPositionsList.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL)
    list = []
    ords = cur.fetchall()
    for ord in ords:
        list.append([ord[0], ord[1], ord[2]])
    con.close()
    return list

#Вернет сообщение с заказом юзера
def GetPositionsListForUser(order_id, id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetPositionsListForUser.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id":order_id, "id": id})
    ords = cur.fetchall()
    list = []
    for ord in ords:
        list.append([ord[0], ord[1], ord[2]])
    con.close()
    return list

#Вернет список с информацией по заведению
def GetShopInfo(shop_id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetShopInfo.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"shop_id": shop_id})
    otv = cur.fetchone()
    con.close()
    return otv

#Вернет общую сумму по заказу
def GetSumma(order_id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetSumma.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id": order_id})
    ords = cur.fetchone()
    con.close()
    return ords[0]

#Вернет сумму юзера по заказу
def GetSummaForUser(order_id, id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetSummaForUser.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id": order_id, "id": id})
    ords = cur.fetchone()
    con.close()
    return ords[0]

#Вернет инфо юзера по его айди
def GetUserInfo(id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetUserInfo.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"id": id})
    otv = cur.fetchone()
    con.close()
    return otv

#Вернет список заведений
def GetShopsList():
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetShopsList.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL)
    list = []
    for s in cur.fetchall():
        list.append([s[0], s[1]])
    con.close()
    return list

#Проставляет дату окончания заказа
def SetOrderStop(order_id):
    order_id = GetOpenOrderID()
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/SetOrderStop.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id": order_id})
    con.commit()
    con.close()


def UpdateOrderTailNULL(user_id, count):
    order_id = GetOpenOrderID()
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/UpdateOrderTailNULL.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id": order_id, "user_id": user_id, "count": count})
    con.commit()
    con.close()


def GetUserList():
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetUserList.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL)
    list = []
    for user_id in cur.fetchall():
        list.append(user_id[0])
    con.close()
    return list


#Вернет список с информацией по заказу
def GetOrderInfo(order_id):
    con = sqlite3.connect('bd_eat.db')
    cur = con.cursor()
    f = open('SQL/GetOrderInfo.sql', 'r')
    SQL = f.read()
    f.close()
    cur.execute(SQL, {"order_id": order_id})
    otv = cur.fetchone()
    con.close()
    return [otv[0], otv[1]]