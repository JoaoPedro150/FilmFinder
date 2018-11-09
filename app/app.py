import controller
import messenger_api

from flask import Flask
from flask import request
from threading import Thread

app = Flask(__name__)

@app.route('/', methods=['POST'])
def post():
    Thread(target=controller.nova_mensagem,args=([request._get_current_object()])).start()

    return '', 200

@app.route('/', methods=['GET'])
def get():
    return messenger_api.autenticacao(request._get_current_object())

if __name__ == '__main__':
    app.run(port=8080, debug=True)
