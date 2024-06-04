from flask import Flask, request, jsonify, send_file
import folium
import io
from PIL import Image


app = Flask(__name__)

BEARER_TOKEN = "teste"

@app.route('/')
def home():
    return "teste"

@app.route('/about')
def about():
    return 'About'

def token_required(f):
    def decorator(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith("Bearer "):
            return jsonify({'error': 'Token ausente ou inválido'}), 401
        token = auth.split(" ")[1]
        if token != BEARER_TOKEN:
            return jsonify({'error': 'Token inválido'}), 403
        return f(*args, **kwargs)
    return decorator



from flask import send_file
import os

@app.route('/sum', methods=['POST'])
@token_required
def sum_values():
    data = request.get_json()
    if 'long' in data and 'lat' in data:
        long = data['long']
        lat = data['lat']
        m = folium.Map(location=(long, lat))

        html_string = m.get_root().render()

        #return send_file('index.py', mimetype='text/x-python')
        return html_string
    else:
        return jsonify({'error': 'Both long and lat are required'}), 400
