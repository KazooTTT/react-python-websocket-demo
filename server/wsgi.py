import eventlet

import threading
import time
from flask_socketio import SocketIO, join_room, send_from_directory
from flask import Flask, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(
    app, cors_allowed_origins='*', sync_mode='eventlet')


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def static_proxy(path):
    # 在这里发送前端应用的所有文件
    file_name = path.split('/')[-1]
    dir_name = os.path.join(app.static_folder, '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)

@app.route('/test')
def restful_test():  # put application's code here
    send_message_to_client("sessionId", "发送到对应的client")
    return '发送到对应的client'


def test_message_loop():
    # for test
    while True:
        socketio.emit("message", time.strftime("%Y-%m-%dT%H:%M:%S"))
        time.sleep(1)


@socketio.on('connect')
def on_connect(params):
    print(f'on_connect {params}')


@socketio.on('chat_message')
def on_messages(data):
    print("data: {}".format(data))
    print(f"chat_message from {request.sid}")
    if data.get("type") == 'register':
        session_id = data.get("sessionId")
        if session_id:
            join_room(session_id)


@socketio.on('disconnect')
def on_disconnect():
    print(f"disconnect: {request.sid}")


def send_message_to_client(session_id, message):
    print(f"session_id {session_id} {message}")
    socketio.emit("message", message, room=session_id)


if __name__ == '__main__':
    eventlet.monkey_patch()
    threading.Thread(target=test_message_loop).start()
    socketio.run(app, host='0.0.0.0', port="5002", debug=True)
