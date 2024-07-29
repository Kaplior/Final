from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Это добавит необходимые заголовки CORS ко всем маршрутам

@app.route('/', methods=['POST'])
def greet():
    data = request.json
    name = data.get('name', 'World')
    return jsonify(message=f"Hello, {name}!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
