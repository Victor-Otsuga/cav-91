from flask import Flask, request, jsonify
from config import BEARER_TOKEN 

app = Flask(__name__)

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

@app.route('/sum', methods=['POST'])
@token_required
def sum_values():
    data = request.get_json()
    if 'value1' in data and 'value2' in data:
        value1 = data['value1']
        value2 = data['value2']
        sum_result = value1 + value2
        return jsonify({'sum': sum_result})
    else:
        return jsonify({'error': 'Both value1 and value2 are required'}), 400

if __name__ == '__main__':
    app.run(debug=True)
