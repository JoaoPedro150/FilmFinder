#Python libraries that we need to import for our bot
import random
import json
import config

from flask import Flask
from flask import request
from flask import abort
from pymessenger.bot import Bot

ACCESS_TOKEN = config.ACCESS_TOKEN
VERIFY_TOKEN = config.VERIFY_TOKEN

app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)

# Aqui chegaram as mensagens enviadas pelo Facebook
@app.route("/", methods=['GET', 'POST'])
def recebe_mensagem():
    if request.method == 'GET':
        return autenticacao()
    else:
        return interpreta_mensagem() 

# Verifica se a requisição veio do Facebook
def autenticacao():
    return request.args.get("hub.challenge") if request.args.get("hub.verify_token") == VERIFY_TOKEN else abort(403)

def interpreta_mensagem():
    output = request.get_json()

    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text') is not None:
                    bot.send_text_message(recipient_id, "Mensagem a ser enviada")
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    bot.send_text_message(recipient_id, "Mensagem a ser enviada")

    return "", 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)