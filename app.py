from flask import render_template
from flask_socketio import SocketIO, emit

from web_chatroom import create_app
import logging

app = create_app()
socketio = SocketIO(app)
app.logger.setLevel(logging.DEBUG)
log = app.logger


@app.route('/', methods=['POST', 'GET'])
def index():
    log.debug("app=%s", app)
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
    log.debug(data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
