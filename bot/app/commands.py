import re
from app import app, bot, log
from app.utils.decorators import admins_only
from app.utils.services import (clear, mute, mute_latest, show_all, show_muted,
                                show_unmuted, unmute, unmute_latest)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Посыльный готов нести службу! 🏃")

@bot.message_handler(commands=['help'])
def send_help(message):
    data = '''
/help - Список доступных команд
/info - Выбранные чаты (DEV/MAIN)
/init - Обозначить текущий чат как MAIN
/services - Показать все доступные сервисы
/clear - Отчистить список сервисов
/muted - Показать сервисы с отключенными оповещениями
/unmuted - Показать сервисы с включенными оповещениями
/mute *service_name* - Заглушить сервис по названию
/unmute *service_name* - Включить оповещения для сервиса по названию
/mute - Заглушить последний сервис
/unmute - Включить оповещения для последнего сервиса
'''
    bot.send_message(message.chat.id, data, parse_mode='Markdown')

@bot.message_handler(commands=['info'])
@admins_only
def send_info(message):
    if app.config['MAIN_CHAT'] == '':
        BOT_INFO = "Главный чат не назначен"
    else:
        BOT_INFO = """
        Главный чат: {}
        Dev-чат: {}
        """.format(app.config['MAIN_CHAT'], app.config['DEV_CHAT'])
    bot.send_message(message.chat.id, BOT_INFO)


@bot.message_handler(commands=['init'])
@admins_only
def get_chat_id(message):
    app.config['MAIN_CHAT'] = message.chat.id
    bot.send_message(message.chat.id, "ID чата сохранен: {}".format(
        app.config['MAIN_CHAT']))


@bot.message_handler(commands=['services'])
@admins_only
def show_all_services(message):
    data = ''
    all_services = show_all()
    if all_services:
        data = 'Все сервисы:\n' + all_services
    else:
        data = 'Сервисы отсутствуют'
    bot.send_message(message.chat.id, data, parse_mode='Markdown')


@bot.message_handler(commands=['muted'])
@admins_only
def show_muted_services(message):
    data = ''
    all_services = show_muted()
    if all_services:
        data = 'Отключенные сервисы:\n' + all_services
    else:
        data = 'Сервисы отсутствуют'
    bot.send_message(message.chat.id, data, parse_mode='Markdown')


@bot.message_handler(commands=['unmuted'])
@admins_only
def show_unmuted_services(message):
    data = ''
    all_services = show_unmuted()
    if all_services:
        data = 'Включенные сервисы:\n' + all_services
    else:
        data = 'Сервисы отсутствуют'
    bot.send_message(message.chat.id, data, parse_mode='Markdown')


@bot.message_handler(commands=['clear'])
@admins_only
def clear_all_services(message):
    clear()
    data = 'Все сервисы удалены'
    bot.send_message(message.chat.id, data)


@bot.message_handler(regexp="/mute (.*)")
@admins_only
def mute_service_by_name(message):
    service = re.findall(r'/mute (.*)', message.text)[0]
    mute(service)


@bot.message_handler(regexp="/unmute (.*)")
@admins_only
def unmute_service_by_name(message):
    service = re.findall(r'/unmute (.*)', message.text)[0]
    unmute(service)


@bot.message_handler(commands=['mute'])
@admins_only
def mute_latest_service(message):
    mute_latest()


@bot.message_handler(commands=['unmute'])
@admins_only
def unmute_latest_service(message):
    unmute_latest()


@bot.message_handler(commands=['test'])
def test(message):
    bot.reply_to(message, "NE TEST")
