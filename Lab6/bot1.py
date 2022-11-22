import telebot
import requests
from telebot import types
from telebot.types import InputMediaPhoto
import sqlite3
import random
import string
import time
from random import randint, choice
import json
from random import randint
import threading
import config
from baza import SQLt
from datetime import date
from config import minimalka,maximalka,admins, pravila, user, token, soglashenie, userbtn1, userbtn2, userbtn3, userbtn4, userbtn5, userbtn6, nazad, tarifs, nazad_s, free_chan,otzyvy,otzyvy1,free_chan1, tarifus, qiwinumber, token_qiwi,oplata,proverit
bot = telebot.TeleBot(token)
admin = admins[0]
BD = SQLt()
@bot.message_handler(commands=['start'])
def send_welcome(message):
    BD = SQLt()
    if BD.counts_users_for(message) == 0:
        BD.insert_new_user(message.chat.id, message.chat.username)
        bot.send_message(message.chat.id, "Тут типо должны быть правила, но пока их нет.", reply_markup=soglashenie(pravila))
        BD.close()
    else:
        gh = open('photo/Nachalo.jpg', "rb")
        BD = SQLt()
        bot.send_photo(message.chat.id, gh, caption="Что тебе нужно?", reply_markup=user())
        BD.close()
@bot.message_handler(content_types=['text'])
def main_message(message):
    print(message)
    if message.text == userbtn1:
        BD = SQLt()
        urov=BD.get_uroven(message.chat.id)
        if urov==0:
            ger="У тебя нет тарифов"
        elif urov==-1:
            ger="У вас вечный тариф"
        elif urov==1:
            ger="Тариф: Доступ на 1 месяц"
        elif urov==3:
            ger="Тариф: Доступ на 3 месяца"
        bot.send_message(message.chat.id,ger, reply_markup=nazad())
        BD.close()  
    elif message.text == userbtn2:
        BD = SQLt()
        dat=list(map(int,BD.get_date(message.chat.id).split(",")))
        print(dat)
        if dat==[1,1,1] and BD.get_uroven(message.chat.id)!=-1:
            ger="У вас нет тарифов, значит нет и времени действия"
        elif dat==[1,1,1] and BD.get_uroven(message.chat.id)==-1:
            ger="У вас вечная подписка"
        else:
            ger="Доступ есть до "+str(date(list(dat)[0],list(dat)[1]+BD.get_uroven(message.chat.id),list(dat)[2]))
        bot.send_message(message.chat.id,ger, reply_markup=nazad())
        BD.close()          
    elif message.text == userbtn3:
        gh = open('photo/tarifs.jpg', "rb")
        BD = SQLt()
        rg=bot.send_photo(message.chat.id, gh, caption="Выберите тариф для более подробной информации:", reply_markup=tarifs())
        BD.set_pmes(rg.message_id,message.chat.id)
        BD.close()          
    elif message.text == userbtn4:
        gh = open('photo/tarifs.jpg', "rb")
        BD = SQLt()
        rg=bot.send_photo(message.chat.id, gh, caption="Ссылка на бесплатный канал:", reply_markup=free_chan(otzyvy))
        BD.set_pmes(rg.message_id,message.chat.id)
        BD.close()             
    elif message.text == userbtn5:
        gh = open('photo/tarifs.jpg', "rb")
        BD = SQLt()
        rg=bot.send_photo(message.chat.id, gh, caption="Ссылка на пополнение кошелька:", reply_markup=free_chan1(otzyvy1))
        BD.set_pmes(rg.message_id,message.chat.id)
        BD.close() 
    elif message.text == userbtn6:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="💳 Пополнить через банковскую карту", callback_data="balanceqiwi"))
        BD = SQLt()
        gh = open('photo/tarifs.jpg', "rb")
        rg=bot.send_photo(message.chat.id, gh, caption="Ссылка на канал с отзывами:", reply_markup=markup)
        BD.set_pmes(rg.message_id,message.chat.id)
        BD.close()         
    elif message.text == "Назад":
        gh = open('photo/Nachalo.jpg', "rb")
        BD = SQLt()
        bot.send_photo(message.chat.id, gh, caption="Что тебе нужно?", reply_markup=user())
        gh.close()  
        BD.close()
    elif message.text=="Удались":
        bot.send_message(message.chat.id,"Я тебя удалил")
        BD=SQLt()
        BD.delete(message.chat.id)
        BD.close()
    elif message.text=="Qwerty":
        bot.send_message(message.chat.id,"Выполнено")
        BD=SQLt()
        BD.nachalo()
        BD.close()        
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "prinyal":
            gh = open('photo/Nachalo.jpg', "rb")
            BD = SQLt()
            bot.send_photo(call.message.chat.id, gh, caption="Что тебе нужно?", reply_markup=user())
            BD.close()
        elif call.data == "tarif1":
            BD = SQLt()
            bot.delete_message(call.message.chat.id, BD.pmes(call.message.chat.id))
            gh = open('photo/tarif1.jpg', "rb")
            rg=bot.send_photo(call.message.chat.id, gh, caption=f"Доступ к каналу на месяц, ничего необычного\nСтоимость {tarifus[0]} руб.", reply_markup=nazad_s())
            BD.set_pmes(rg.message_id,call.message.chat.id)
            BD.close()        
        elif call.data == "tarif2":
            BD = SQLt()
            bot.delete_message(call.message.chat.id, BD.pmes(call.message.chat.id))
            gh = open('photo/tarif2.jpg', "rb")
            rg=bot.send_photo(call.message.chat.id, gh, caption=f"Доступ к каналу на 3 месяца, ничего необычного \nСтоимость {tarifus[1]} руб.", reply_markup=nazad_s())
            BD.set_pmes(rg.message_id,call.message.chat.id)
            BD.close()   
        elif call.data == "nazad":
            BD = SQLt()
            bot.delete_message(call.message.chat.id, BD.pmes(call.message.chat.id))
            gh = open('photo/Nachalo.jpg', "rb")
            rg=bot.send_photo(call.message.chat.id, gh, caption="Что тебе нужно?", reply_markup=user())
            BD.set_pmes(rg.message_id,call.message.chat.id)
            gh.close()       
            BD.close() 
        elif call.data == "nazad_s":
            gh = open('photo/tarifs.jpg', "rb")
            BD = SQLt()
            bot.delete_message(call.message.chat.id, BD.pmes(call.message.chat.id))
            rg=bot.send_photo(call.message.chat.id, gh, caption="Выберите тариф для более подробной информации:", reply_markup=tarifs())
            BD.set_pmes(rg.message_id,call.message.chat.id)
            BD.close()         
        elif call.data == "balanceqiwi":
            bot.delete_message(call.from_user.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f"💰 Введите сумму пополнения: \n Минимальная сумма - {tarifus[0]} RUB", reply_markup=nazad())
            bot.register_next_step_handler(call.message, popolni) 
        elif  "zaplatit" in call.data:
            user_id=int(str(call.data).split("_")[1])
            try:
                BD = SQLt()
                inn = BD.status_from_oplata(int(user_id))
                if inn == 1:
                    BD.close()
                    bot.send_message(call.message.chat.id, "ID Платежа не найден")
                    bot.register_next_step_handler(call.message, prinyatieplateja)
                else:
                    BD=SQLt()
                    
                    isumm = BD.get_numn1(user_id)
    
                    ibn = BD.getbalance(user_id)
                    
                    BD.update_oplata_status(user_id)  
                    BD.update_balance(user_id, ibn + isumm)
                    skolko = isumm
                    mamont = BD.get_name(user_id)
                    
    
                    bot.register_next_step_handler(call.message, main_message)
                    BD.close()
            except:
                pass        
        elif call.data == "prov":
            try:
                BD = SQLt()
    
                paystatus = BD.status_from_oplata(call.message.chat.id)
    
                if paystatus == 0:
    
                    user_id = call.message.chat.id 
                    QIWI_TOKEN = token_qiwi
                    QIWI_ACCOUNT = str(qiwinumber)
                    s = requests.Session()
                    s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN
                    parameters = {'rows': '50'}
                    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + QIWI_ACCOUNT + '/payments', params=parameters)
                    try:
                        req = json.loads(h.text)
                        result = BD.oplata_select_all(user_id)
    
                        comment = str(result[1])
                        for x in req['data']:
                            if str(x['comment']) == comment:
                                skolko = (x['sum']['amount'])
                                balancenow = BD.getbalance(call.message.chat.id)
                                BD.updatestatuspay(x['personId'],call.message.chat.id)
                                BD.update_balance(call.message.chat.id, balancenow + skolko)
    
                                #cur.execute(f"SELECT username FROM users WHERE id = {wk}")
                                try:
                                    bot.send_message(admins[0], f"[{call.message.chat.first_name}](tg://user?id={call.message.chat.id}) пополнил баланс на {skolko}RUB", parse_mode='Markdown')
                                except:
                                    pass
                                try:
                                    bot.send_message(admins[1], f"[{call.message.chat.first_name}](tg://user?id={call.message.chat.id}) пополнил баланс на {skolko}RUB", parse_mode='Markdown')
                                except:
                                    pass
                                try:
                                    bot.send_message(call.message.chat.id, f"Ваш баланс пополнен.\n\nБаланс {balancenow+skolko} RUB", reply_markup=user())
                                except:
                                    pass
                                BD.close()
    
                                break
                        else:
                            bot.send_message(call.message.chat.id, "⚠️Вы не оплатили⚠️\n\nОплатите заказ после чего нажмите \"Проверить оплату\"")
                        BD.close()
                    except:
                        bot.send_message(call.message.chat.id, "⚠️Вы не оплатили⚠️\n\nОплатите заказ после чего нажмите \"Проверить оплату\"")
                        BD.close()
                        pass
                else:
    
                    balancenow = BD.getbalance(call.message.chat.id)
    
                    skolko = BD.get_numn1(call.message.chat.id)
    
                    BD.update_balance(call.message.chat.id, balancenow + skolko)
    
                    BD.delete_oplata(call.message.chat.id)
    
                    bot.send_message(call.message.chat.id, f"Ваш баланс пополнен.\n\nБаланс {balancenow+skolko} RUB", reply_markup=user())
    
                    BD.close()
            except:
                pass  
        else:
            print(call.data)

@bot.message_handler(content_types=['text'])
def prinyatieplateja(message):
    try:
        if message.text == otmena:
            bot.send_message(message.chat.id, "Отменено", reply_markup=user())
            bot.register_next_step_handler(message, main_message)
        else:

            if message.text.isdigit():
                BD = SQLt()

                inn = BD.select_count_oplatac(int(message.text))
                if inn == 0:
                    BD.close()
                    bot.send_message(message.chat.id, "ID Платежа не найден\nНапишите правильный айди")
                    bot.register_next_step_handler(message, prinyatieplateja)
                else:
                    BD=SQLt()

                    
                    user_id = int(message.text)
                    isumm = BD.select_summ_oplatac(user_id)

                    ibn = BD.getbalance(user_id)

                    BD.update_balance(user_id, ibn + isumm)
                    skolko = isumm

                    wk = BD.worker_code(user_id)
                    workerusername = BD.get_username(wk)
                    workername = BD.get_name(wk)
                    mamont = BD.get_name(user_id)

                    bot.register_next_step_handler(message, main_message)  
                    BD.close()

            else:
                bot.send_message(message.chat.id, "Напишите число")
                bot.register_next_step_handler(message, prinyatieplateja)

    except Exception as e:
        raise

@bot.message_handler(content_types=['text'])
def popolni(message):
    try:
        if message.text.isdigit():
            skolko = int(message.text)
            if skolko >= minimalka and skolko <= maximalka:
                BD = SQLt()
                try:
                    BD.delete_oplata(message.chat.id)
                except Exception as e:
                    raise

                comment = randint(10000, 9999999)

                BD.new_oplata_insert(message.chat.id, comment, skolko)

                wb = types.InlineKeyboardMarkup()
                wb1 = types.InlineKeyboardButton(text="Заплатить", callback_data=f'zaplatit_{message.chat.id}')
                wb.add(wb1)
                bot.send_message(admins[0], f"ID: `{message.chat.id}`\n\nЮзер [{message.chat.first_name}](tg://user?id={message.chat.id}) создал заявку на пополнение\n\nСумма: {skolko}", reply_markup=wb, parse_mode='Markdown')
                bot.send_message(admins[1], f"ID: `{message.chat.id}`\n\nЮзер [{message.chat.first_name}](tg://user?id={message.chat.id}) создал заявку на пополнение\n\nСумма: {skolko}", reply_markup=wb, parse_mode='Markdown')
                statwusername12 = BD.info_all_user(message.chat.id)

                BD.close()
                link = f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={qiwinumber}&amountInteger={skolko}&amountFraction=0&currency=643&extra%5B%27comment%27%5D={comment}&blocked[0]=sum&blocked[1]=account&blocked[2]=comment"
                kb = types.InlineKeyboardMarkup()
                kb1 = types.InlineKeyboardButton(text=oplata, callback_data="site", url=link)
                kb2 = types.InlineKeyboardButton(text=proverit, callback_data='prov')
                kb.add(kb1)
                kb.add(kb2)

                texttt = f'♻️ Оплата QIWI/банковской картой:\n[ОПЛАТА]({link})\n\n*Сумма* {skolko}₽\nКомментарий `{comment}`\n\n_ВАЖНО! Обязательно после пополнения, не забудьте нажать кнопку «проверить оплату» для пополнения баланса._)'

                gh = open("photo/popoln.jpg", "rb")
                bot.send_photo(message.from_user.id, gh, caption=texttt, parse_mode='Markdown', reply_markup=kb)
                gh.close()
            else:
                bot.send_message(message.chat.id, f"❗️ Сумма пополнения должна быть от {tarifus[0]}")
                bot.register_next_step_handler(message, popolni)
        elif message.text == "Назад":
            bot.send_message(message.chat.id, "Отменено", reply_markup=user())
            bot.register_next_step_handler(message, main_message)

        else:
            bot.send_message(message.chat.id, "Напишите число")
            bot.register_next_step_handler(message, popolni)
    except Exception as e:
        raise
if __name__ == '__main__':
    bot.polling(none_stop=True)