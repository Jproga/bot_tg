import telebot, config
import time, threading, schedule

from random import choice

API_TOKEN = config.token

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет, я info_bot.
Я здесь, чтобы ответить вам добрыми словами. Просто скажите что-нибудь приятное, и я скажу вам то же самое!\
""")

@bot.message_handler(commands=['help'])
def send_welcome_2(message):
    bot.reply_to(message, "В боте есть команды /set, /unset, /coin, /fact, /clothes_color, /clothes_brand,")


def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='izi!')


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


@bot.message_handler(commands=['coin'])
def coin_handler(message):
    coin = choice(["ОРЕЛ", "РЕШКА"])
    bot.reply_to(message, coin)

@bot.message_handler(commands=['fact'])
def fact_handler(message):
    fact = choice([
        "Ханс Кристиан Андерсен не мог грамотно написать практически ни одного слова.", " Самый большой динозавр из когда-либо обнаруженных достигал в длину более тридцати метров и весил более восьмидесяти тонн.", "Ночью Млечный путь выглядит как вытянутое туманное облако, состоящее из более чем двухсот миллиардов звёзд.",
        "Земля - единственная планета солнечной системы, которую не назвали в честь бога.", "Продолжительность первого выхода в космос Леоновым составила двенадцать минут", "В молодости черноморские окуни в основном самки, но уже к пяти годам они радикально меняют пол.",
        "Во время второй мировой войны первая бомба, сброшенная на Берлин, убила единственного слона в Берлинском зоопарке.", "Почти тридцать процентов женщин, узнав, что выиграли в лотерею, прячут выигрышный билет в лифчик.", " С ноября тысяча девятьсот сорок первого года в Советском Союзе был налог на бездетность. Он составлял шесть процентов от всей зарплаты.",
        "В среднем одинокие мужчины на два с половиной сантиметра ниже ростом, чем женатые.", "Ежедневная двадцатиминутная прогулка сжигает около трех килограмм жира в год.", "В ходе массового опроса секретарш, проведенного американскими социальными психологами, девяносто два процента респонденток заявили, что они 'не прочь завести роман' со своим шефом.",
        "Автором электрического стула был простой дантист.", "Длина всех кровеносных сосудов человеческого тела — около девяносто шести тысяч километров.", "Ушная сера необходима для здоровья ушей.",
        ])
    bot.reply_to(message, fact)

@bot.message_handler(commands=['clothes_color'])
def clothes_color(message):
    clothes_color = choice(["красный", "синий", "желтый", "белый", "оранжевый", "черный", "фиолетовый"])
    bot.reply_to(message, clothes_color)

@bot.message_handler(commands=['clothes_brand'])
def clothes_brand(message):
    clothes_brand = choice(["nike", "gucci", "puma", "adidas", "the north face", "lacoste", "shanel"])
    bot.reply_to(message, clothes_brand)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)   


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)