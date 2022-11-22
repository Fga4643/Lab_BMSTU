import sqlite3

import config

import telebot
from telebot import types
from config import token
from datetime import date

bot = telebot.TeleBot(token) 

class SQLt():
    def __init__(self):
        self.connection = sqlite3.connect("data.db")
        self.cursor = self.connection.cursor()
    def nachalo(self):
        with self.connection:
            self.cursor.execute('''CREATE TABLE user (id int)''')
            self.cursor.execute("ALTER TABLE user ADD column 'uroven1' 'int'")
            self.cursor.execute("ALTER TABLE user ADD column 'date' 'str'")
            self.cursor.execute("ALTER TABLE user ADD column 'name' 'str'")
            self.cursor.execute("ALTER TABLE user ADD column 'pmes' 'int'")
            self.cursor.execute("ALTER TABLE user ADD column 'balance' 'int'")
            self.cursor.execute('''CREATE TABLE oplata (id int)''')
            self.cursor.execute("ALTER TABLE oplata ADD column 'code' 'int'")
            self.cursor.execute("ALTER TABLE oplata ADD column 'status' 'int'")
            self.cursor.execute("ALTER TABLE oplata ADD column 'summ' 'int'")  
            self.cursor.execute('''CREATE TABLE oplatac (id int)''')
            self.cursor.execute("ALTER TABLE oplatac ADD column 'summ' 'int'")            
    def new_oplata_insert(self, user_id, commet, skolko):
        with self.connection:
            self.cursor.execute(f"INSERT INTO oplata (id, code,status,summ) VALUES({user_id},{commet},{0},{skolko})")            
    def counts_users_for(self, message):
        with self.connection:
            return self.cursor.execute(f"SELECT count(*) FROM user WHERE id = {message.chat.id}").fetchone()[0] 
    def dobav(self):
        self.cursor.execute("ALTER TABLE user ADD column 'date' 'date'")
    def insert_new_user(self, id, name):
        with self.connection:
            q=str(date.today())
            self.cursor.execute(f"INSERT INTO user (id,name,uroven1,date,pmes,balance)"
                                f"VALUES ({id},\"{name}\",{0},\"1,1,1\",0,0)")
    def delete(self,ids):
        with self.connection:
            self.cursor.execute(f"DELETE FROM user WHERE id ={ids}")
    def get_uroven(self, ids):
        with self.connection:
            return self.cursor.execute(f"SELECT uroven1 from user where id ={ids}").fetchone()[0]
    def get_name(self, ids):
        with self.connection:
            return self.cursor.execute(f"SELECT name from user where id ={ids}").fetchone()[0]
    def get_date(self,ids):
        with self.connection:
            return self.cursor.execute(f"SELECT date from user where id ={ids}").fetchone()[0]
    def pmes(self,ids):
        with self.connection:
            return self.cursor.execute(f"SELECT pmes from user where id ={ids}").fetchone()[0]
    def set_pmes(self,pmes,ids):
        with self.connection:
            self.cursor.execute("UPDATE user SET pmes = ? WHERE id = ?",(str(pmes),str(ids)))
    def insert_new_oplatac(self, user_id, skolko):
        with self.connection:
            self.cursor.execute(f"INSERT INTO oplatac (id,summ) VALUES({user_id},{skolko})")
    def get_id_oplatac(self, user_id):
        with self.connection:
            return self.cursor.execute(f"select id from oplatac where id = {user_id}").fetchone()[0]

    def select_summ_oplatac(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT summ FROM oplatac WHERE id = {user_id}").fetchone()[0]
    def info_all_user(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM user where id = {user_id}").fetchone()    
    def select_count_oplatac(self, user_id):
        with self.connection:
            return self.cursor.execute(f"select count(*) from oplatac where id = {user_id}").fetchone()[0]            
    def get_numn(self, chat_id):
        with self.connection:
            return self.cursor.execute(f"select summ from oplatac WHERE id = {chat_id}").fetchone()[0]    
    def delete_oplatac(self, user_id):
        with self.connection:
            self.cursor.execute(f"DELETE from oplatac where id = {user_id}")    
    def status_from_oplata(self, user_id):
        with self.connection:
            return self.cursor.execute(f"select status from oplata where id = {user_id}").fetchone()[0]    
    def update_oplata_status(self, user_id):
        with self.connection:
            self.cursor.execute(f"UPDATE oplata SET status = {1} where id = {user_id}")    
    def oplata_select_all(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM oplata WHERE id = {user_id}").fetchone()   
    def get_numn1(self, user_id):
        with self.connection:
            return self.cursor.execute(f"select summ from oplata WHERE id = {user_id}").fetchone()[0]    
    def updatestatuspay(self, ids, status):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `statuspay` = ? WHERE `id` = ?", (status, ids))
    def update_balance(self, user_id, balance_up):
        with self.connection:
            self.cursor.execute(f"UPDATE user SET balance = {balance_up} WHERE id = {user_id}")    
    def delete_oplata(self, user_id):
        with self.connection:
            self.cursor.execute(f"DELETE FROM oplata WHERE id = {user_id}")    
    def getbalance(self, msid):
        with self.connection:
            self.cursor.execute(f"select balance from user WHERE id = {msid}")
            return self.cursor.fetchone()[0]        
    def close(self):
        self.connection.close()    