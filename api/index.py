from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "teste"

@app.route('/about')
def about():
    return 'About'

@app.route('/sum', methods=['POST'])
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
