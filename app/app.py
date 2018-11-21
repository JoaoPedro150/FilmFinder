import controller
import messenger_api
import os

from flask import Flask
from flask import request
from flask import abort
from threading import Thread

app = Flask(__name__)

@app.route('/', methods=['POST'])
def post():
    Thread(target=controller.nova_mensagem,args=([request._get_current_object()])).start()

    return '', 200

@app.route('/', methods=['GET'])
def get():
    status = messenger_api.autenticacao(request._get_current_object())
    if status[1] == 200: return status
    abort(403)

if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT")), host='0.0.0.0')
