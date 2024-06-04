from flask import Flask

app = Flask(__name__)

@app.route('/', methods = 'POST')
def home():
    return "teste"

@app.route('/about')
def about():
    return 'About'