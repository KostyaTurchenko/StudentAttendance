from app import app
from flask import jsonify


@app.route('/')
@app.route('/main.html')
def main_page():
    return "Hi my freands!"

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')