import telebot
import sqlite3
import time
import random
import string

TOKEN = "8631214794:AAFaddS-36TpPtTUUY-CvddCDQuhIFCJdEA"
OWNER_ID = 5168499996

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, expire INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS keys (key TEXT, expire INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS banned (id INTEGER)")
conn.commit()

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Welcome to the bot")

@bot.message_handler(commands=['gen48'])
def gen48(msg):
    if msg.from_user.id != OWNER_ID:
        return
    key = generate_key()
    expire = int(time.time()) + 483600
    cursor.execute("INSERT INTO keys VALUES (?,?)", (key, expire))
    conn.commit()
    bot.reply_to(msg, f"Key 48H:\n{key}")

@bot.message_handler(commands=['gen7d'])
def gen7d(msg):
    if msg.from_user.id != OWNER_ID:
        return
    key = generate_key()
    expire = int(time.time()) + 724*3600
    cursor.execute("INSERT INTO keys VALUES (?,?)", (key, expire))
    conn.commit()
    bot.reply_to(msg, f"Key 7D:\n{key}")

@bot.message_handler(commands=['redeem'])
def redeem(msg):
    try:
        key = msg.text.split()[1]
    except:
        bot.reply_to(msg, "Send: /redeem KEY")
        return

    cursor.execute("SELECT * FROM keys WHERE key=?", (key,))
    data = cursor.fetchone()

    if not data:
        bot.reply_to(msg, "Invalid key")
        return

    expire = data[1]

    cursor.execute("INSERT INTO users VALUES (?,?)", (msg.from_user.id, expire))
    cursor.execute("DELETE FROM keys WHERE key=?", (key,))
    conn.commit()

    bot.reply_to(msg, "Key activated")

@bot.message_handler(commands=['ban'])
def ban(msg):
    if msg.from_user.id != OWNER_ID:
        return
    try:
        uid = msg.text.split()[1]
    except:
        return

    cursor.execute("INSERT INTO banned VALUES (?)", (uid,))
    conn.commit()
    bot.reply_to(msg, "User banned")

@bot.message_handler(func=lambda m: True)
def check_user(msg):

    cursor.execute("SELECT * FROM banned WHERE id=?", (msg.from_user.id,))
    if cursor.fetchone():
        return

    cursor.execute("SELECT * FROM users WHERE id=?", (msg.from_user.id,))
    data = cursor.fetchone()

    if not data:
        bot.reply_to(msg, "You don't have access")
        return

    if int(time.time()) > data[1]:
        bot.reply_to(msg, "Your subscription expired")
        return

    bot.reply_to(msg, "Bot working")

bot.infinity_polling()
