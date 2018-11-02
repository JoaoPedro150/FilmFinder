import messenger_platform

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def post():
    return messenger_platform.nova_mensagem(request._get_current_object())

@app.route('/', methods=['GET'])
def get():
    return messenger_platform.autenticacao(request._get_current_object())

if __name__ == '__main__':
    app.run(port=8080, debug=True)