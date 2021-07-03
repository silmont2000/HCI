from flask import render_template
from web_chatroom import create_app, socketio

app = create_app()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on("client_send")
def client_send(data):
    # if msg is blank, do not emit
    if data['msg'] != '':
        socketio.emit('server_response',
                      {'id': id, 'user': data['user'], 'time': data['time'],
                       'msg': data['msg']}, namespace='\msg')


if __name__ == '__main__':
    socketio.run(app, debug=True)
