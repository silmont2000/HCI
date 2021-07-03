from flask import Blueprint, render_template

chat = Blueprint('chat', __name__)


@chat.route('/chatroom', methods=['POST', 'GET'])
def chatroom():
    return render_template('/chatroom.html')
