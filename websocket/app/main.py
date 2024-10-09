from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", transports=['websocket', 'polling'])

@socketio.on('message')
def handle_message(msg):
    print('Message received: ' + msg)
    send(msg, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return jsonify({"message":"Welcome to Flask WebSocket Example!"})

 # pip freeze > requirements.txt
# pip install - r requirements.txt

if __name__ == '__main__':
    socketio.run(app, debug=True)
