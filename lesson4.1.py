import telebot
import sqlite3

bot = telebot.TeleBot("6608715523:AAF9rMJd4RPqsLgFxaVTiu9-O0L9sfGLhHE")
name = None


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('some_base.sql')
    cur = conn.cursor()

    # Выводим список пользователей, если нажали на кнопку 'Список пользователей'
    if call.data == 'users':
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        # Создание кнопок. Сперва создаем markup
        markup = telebot.types.InlineKeyboardMarkup()

        for el in users:
            # через цикл создаем кнопки и добавляем внутрь markup
            # при нажатии на кнопки будет вызван этот же метод def callback(call):
            markup.add(telebot.types.InlineKeyboardButton(el[1], callback_data=str(el[0])))

        bot.send_message(call.message.chat.id, 'Все пользователи:', reply_markup=markup)
    else:
        # получение одной записи по ID
        cur.execute("SELECT * FROM users WHERE `id` = '%s'" % call.data)
        user = cur.fetchone()
        bot.send_message(call.message.chat.id, f'Пользователь: {user[1]}, password: {user[2]}')

    cur.close()
    conn.close()


bot.polling(none_stop=True)