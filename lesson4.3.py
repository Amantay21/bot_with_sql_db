import telebot
import sqlite3

bot = telebot.TeleBot("6608715523:AAF9rMJd4RPqsLgFxaVTiu9-O0L9sfGLhHE")
name = None
password = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('some_base.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, pass TEXT, progr_lang TEXT)')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Введите ваше имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_lang)

def user_lang(message):
    global password
    password = message.text.strip()
    bot.send_message(message.chat.id, "Введите язык программирования который хотите изучить")
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    programming_lang = message.text.strip()

    conn = sqlite3.connect('some_base.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass, progr_lang) VALUES (?, ?, ?)", (name, password, programming_lang))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='user_list'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'user_list':
        conn = sqlite3.connect('some_base.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        markup = telebot.types.InlineKeyboardMarkup()

        for user in users:
            user_button = telebot.types.InlineKeyboardButton(user[1], callback_data=f'user_{user[0]}')
            markup.add(user_button)

        bot.send_message(call.message.chat.id, 'Список пользователей:', reply_markup=markup)
        cur.close()
        conn.close()
    elif call.data.startswith('user_'):
        user_id = int(call.data.split('_')[1])

        conn = sqlite3.connect('some_base.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE id=?', (user_id,))
        user = cur.fetchone()

        if user:
            user_info = f'Имя: {user[1]}\nПароль: {user[2]}\n Язык прогр-я: {user[3]}'
            bot.send_message(call.message.chat.id, user_info)

        cur.close()
        conn.close()
# bot.ReplyKeyboardRemove(selective=None, *, api_kwargs=None)

bot.polling(none_stop=True)