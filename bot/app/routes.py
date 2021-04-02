import telebot
from flask import (
    abort,
    request,
    render_template,
)
from app import (
    app,
    bot,
    log
)
from app.utils.services import add, is_muted

API_TOKEN = app.config['TG_SECRET_KEY']
SECRET = app.config['SECRET']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/{}'.format(API_TOKEN), methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


@app.route('/{}'.format(SECRET), methods=["POST"])
def dev_webhook():
    if app.config['MAIN_CHAT'] == '':
        log.warn('Init bot first by "/init" command')
        return abort(403)
    if request.headers.get('content-type') == 'application/json':
        jData = request.get_json()
        '''
        Field "message" contains data.
        Main field, without it bot don't send anything. 
        '''    
        if 'message' in jData.keys():
            data = jData['message']
            
            '''
            Field "to" contains destination chat.
            It can be set to "MAIN" or "DEV" for chats from .env.
            Default is "DEV".
            '''
            SEND_TO = app.config['DEV_CHAT']
            if 'to' in jData.keys():
                send_to = jData['to']
                if send_to == 'MAIN':
                    SEND_TO = app.config['MAIN_CHAT']
                elif send_to == 'DEV':
                    SEND_TO = app.config['DEV_CHAT']
                else:
                    SEND_TO = send_to

            '''
            Field "id" contains service name.
            If service is muted than message will be skipped.
            '''
            if 'id' in jData.keys():
                id = jData['id']
                add(id)
                if is_muted(id):
                    return "OK"
            
            '''
            Type can be "markdown/html/plain/file".
            Default type - "plain".
            '''
            if 'type' in jData.keys():
                type = jData['type']
                try:
                    if type == 'markdown':
                        bot.send_message(SEND_TO, data, parse_mode='Markdown')
                        return "OK"
                    elif type == 'html':
                        bot.send_message(SEND_TO, data, parse_mode='HTML')
                        return "OK"
                    elif type == 'plain':
                        bot.send_message(SEND_TO, data)
                        return "OK"
                    elif type == 'file':
                        file = open('/home/app/bot/files/' + data, 'rb')
                        bot.send_document(SEND_TO, file, timeout=60)
                        return "OK"
                except Exception:
                    bot.send_message(SEND_TO, data)
                    return "OK"
            else:
                bot.send_message(SEND_TO, data)
                return "OK"
        else:
            log.error("Wrong json data")
            abort(403)
    else:
        log.error("Wrong content type")
        abort(403)
