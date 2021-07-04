import hashlib
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, r


class User(UserMixin, db.Model):
    """用户表"""
    __tablename__ = "tbl_users"  # 指明数据库的表名

    id = db.Column(db.Integer, primary_key=True)  # 整型的主键， 会默认设置为自增主键
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    avatar = db.Column(db.String(128))

    def __init__(self, *info):
        self.name = info[0]
        self.password = generate_password_hash(info[1])
        self.avatar = self.get_gravatar_url(self.name)
        # self.id = User.get("id")

    def __repr__(self):
        return 'User:%s' % self.name

    def get_id(self):
        """获取用户ID"""
        return self.id

    def get_gravatar_url(self, username='', size=40):
        """返回头像url"""
        styles = ['identicon', 'monsterid', 'wavatar', 'retro']
        '''
        mm： 简约、卡通风格的人物轮廓像（不会随邮箱哈希值变化而变化）。
        identicon：几何图案，其形状会随电子邮箱哈希值变化而变化。
        monsterid：程序生成的“怪兽”头像，颜色和面孔会随会随电子邮箱哈希值变化而变化。
        wavatar:：用不同面容和背景组合生成的面孔头像。
        retro：程序生成的8位街机像素头像。
        '''
        if username == '':
            username = self.name
        m5 = hashlib.md5(f'{username}'.encode('utf-8')).hexdigest()  # 返回16进制摘要字符串
        url = f'http://fdn.geekzu.org/avatar/{m5}?s={size}&d=identicon'
        return url

    def verify_password(self, password):
        """密码验证"""
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password = generate_password_hash(password)


def init_db():
    db.drop_all()
    db.create_all()
    # 测试
    del_user = User.query.filter_by(name='test')
    for i in del_user:
        db.session.delete(i)
    db.session.commit()

    new_user = User('test', '1')
    db.session.add(new_user)
    db.session.commit()


def init_msg():
    # 默认连接池
    r.flushdb()
    r.set('msg', 'flushed msgDB')
    value = r.get('msg')
