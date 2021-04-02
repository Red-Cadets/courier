from flask import Flask
from time import sleep
import logging
import telebot

app = Flask(__name__)
app.config.from_object('config.Config')
app.static_folder = app.config['STATIC_FOLDER']

log = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(app.config['TG_SECRET_KEY'])

API_TOKEN = app.config['TG_SECRET_KEY']
WEBHOOK_HOST = app.config['WEBHOOK_HOST']

bot.remove_webhook()
sleep(1)
bot.set_webhook(url=WEBHOOK_HOST+API_TOKEN)

from app import commands, routes
