from aiogram import Bot
import mysql.connector as mysql_conn
import sqlite3
import configparser

cfg = configparser.ConfigParser()
cfg.read("conf.ini")

bot_token = cfg['default_data']['bot_token']
bot_owner = int(cfg['default_data']['bot_owner'])
log_chat_id = cfg['default_data']['log_chat_id']
errors_chat_id = cfg['default_data']['errors_chat_id']

bot = Bot(token=bot_token)

if "mysql" in cfg.sections():
    db_user = cfg["mysql"]['user']
    db_password = cfg["mysql"]['password']
    db_host = cfg["mysql"]['host']
    db_database = cfg["mysql"]['database']
    db = mysql_conn.connect(user=db_user, password=db_password, database=db_database, host=db_host)
    c = db.cursor(buffered=True)
else:
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()

