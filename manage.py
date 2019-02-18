import redis
from flask import  Flask
from flask_script import Manager
from flask_session import Session

from app.house_views import house_blue
from app.order_views import order_blue
from app.user_views import user_blue
from app.models import db

app = Flask(__name__)

#设置加密的复杂程度
app.secret_key='34asd1as5r4a56$#!@%#$45'

#注册蓝图
app.register_blueprint(blueprint=user_blue,url_prefix='/user')
app.register_blueprint(blueprint=house_blue,url_prefix='/house')
app.register_blueprint(blueprint=order_blue,url_prefix='/order')

#配置数据库

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@127.0.0.1:3306/ihome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#初始化db
db.init_app(app)


app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=redis.Redis(host='127.0.0.1',port=6379)

#配置session
se = Session()
se.init_app(app)

#将app交个manage管理
manage = Manager(app)

if __name__ == '__main__':
    manage.run()