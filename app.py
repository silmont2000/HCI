from flask import render_template
from flask_socketio import SocketIO, emit
from web_chatroom import create_app, r
from flask import current_app

app = create_app()
socketio = SocketIO(app)


# log = current_app.logger


@app.route('/', methods=['POST', 'GET'])
def index():
    current_app.logger.debug("app=%s", app)
    return render_template('index.html')


@socketio.on("client_send")
def client_send(data):
    if data['msg'] != '':
        emit('server_response',
             {'name': data['name'],
              'avatar': data['avatar'],
              'msg': data['msg'],
              'time': data['time'],
              },
             broadcast=True
             )
    current_app.logger.debug(data)


@socketio.on("client_connection")
def join_room(data):
    current_app.logger.debug(data['name'])
    r.sadd('roommate', data['name'])
    r.sadd(data['name'], data['id'])
    value = r.smembers('roommate')
    current_app.logger.debug('目前在线：%s', value)
    current_app.logger.debug('新id：%s', data['id'])


@socketio.on("client_disconnect")
def leave_room(data):
    current_app.logger.debug(data['name'])
    r.srem('roommate', data['name'])
    value = r.smembers('roommate')
    current_app.logger.debug('目前在线：%s', value)
    emit('leave', {'name': data['name']}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
