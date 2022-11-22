from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
token="Токен от бота"
admins=[Id_admin1,Id_admin2]
qiwinumber="Ваш номер"
token_qiwi="Зачем он вам?"
qiwi=""
otzyvy="Ваш канал"
otzyvy1="Ваш канал"
pravila='Принять'
userbtn1 = "🖥Мой тариф🖥"
userbtn2 = "⏱Сколько осталось до конца⏱"
userbtn3 = "🤑Выбор тарифов🤑"
userbtn4 = "😘Мой бесплатный канал😘"
userbtn5 = "💬Отзывы💬"
userbtn6 = "🦾Покупка тарифов🦾"
oplata = "💳 Оплатить"
proverit = "📲 Проверить платёж"
tarifus = [1, 2, 3, 4]
minimalka=1
maximalka=3
def user():
	k1 = types.ReplyKeyboardMarkup(True)
	k1_btn1 = types.KeyboardButton(userbtn1)
	k1_btn2 = types.KeyboardButton(userbtn2)
	k1_btn3 = types.KeyboardButton(userbtn3)
	k1_btn4 = types.KeyboardButton(userbtn4)
	k1_btn5 = types.KeyboardButton(userbtn5)
	k1_btn6 = types.KeyboardButton(userbtn6)
	k1.add(k1_btn1, k1_btn2)
	k1.add(k1_btn3)
	k1.add(k1_btn4, k1_btn5)
	k1.add(k1_btn6)
	return k1
def free_chan(otzyvy):
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton(text="Мы в телеграмм", url=otzyvy))
	return markup
def free_chan1(otzyvy):
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton(text="Мы в телеграмм", url=otzyvy))
	return markup
def soglashenie(prinyat):
	prinyatpravila = types.InlineKeyboardMarkup()
	prinyatpravila_btn1 = types.InlineKeyboardButton(text=prinyat, callback_data="prinyal")
	prinyatpravila.add(prinyatpravila_btn1)
	return prinyatpravila
def nazad():
	k1 = types.ReplyKeyboardMarkup(True)
	k1_btn1 = types.KeyboardButton("Назад")	
	k1.add(k1_btn1)
	return k1
def nazad_s():
	act = types.InlineKeyboardMarkup()
	activ_btn3 = types.InlineKeyboardButton("Назад", callback_data="nazad_s")
	act.add(activ_btn3)
	return act
def tarifs():
	act = types.InlineKeyboardMarkup()
	activ_btn1 = types.InlineKeyboardButton("Тариф 1 месяц", callback_data="tarif1")
	activ_btn2 = types.InlineKeyboardButton("Тариф 3 месяца", callback_data="tarif2")
	activ_btn3 = types.InlineKeyboardButton("Назад", callback_data="nazad")
	act.add(activ_btn1)
	act.add(activ_btn2)
	act.add(activ_btn3)
	return act