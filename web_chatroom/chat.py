from flask import Blueprint, render_template

from web_chatroom import r

chat = Blueprint('chat', __name__)


@chat.route('/chatroom', methods=['POST', 'GET'])
def chatroom():
    user = r.smembers('roommate')
    return render_template('/chatroom.html', user_list=user)
