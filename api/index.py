from flask import Flask

app = Flask(__name__)

@app.route('/', methods = 'POST')
def soma(a,b):
    return a+b

def home():
    c = soma(1,2)
    return "teste"

@app.route('/about')
def about():
    return 'About'