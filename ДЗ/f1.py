from flask import Flask
from Функции.func import fibonacci

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/num/<number>')
def num(number):
    return str(list(fibonacci(int(number))))[1:-1]