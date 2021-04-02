import os
from ast import literal_eval

class Config:
    TG_SECRET_KEY = os.getenv('TG_SECRET_KEY')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY').encode()
    WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
    STATIC_FOLDER = os.getenv('APP_FOLDER') + '/static'
    SECRET = os.getenv('SECRET')
    ADMINS = literal_eval(os.getenv('ADMINS'))
    MAIN_CHAT = os.getenv('MAIN_CHAT')
    DEV_CHAT = os.getenv('DEV_CHAT')
