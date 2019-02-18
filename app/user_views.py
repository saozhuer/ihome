import random
import re
import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash,check_password_hash

from app.models import User, db, House

from utils import status_code
from utils.funtions import is_login

user_blue = Blueprint('user',__name__)




@user_blue.route('/get_code/',methods=['GET','POST'])
def get_code():
    """
    生成验证码
    """
    #生成随机参数，返回给页面，在页面中生成图片
    code = ''
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    for i in range(4):
        code += random.choice(s)
    session['code'] = code
    return jsonify(code=200, msg='请求成功', data=code)


@user_blue.route('/register/',methods=['GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

@user_blue.route('/register/', methods=[ 'POST'])
def my_register():
        #获取页面上的数据
        mobile = request.form.get('mobile')
        imagecode = request.form.get('imagecode')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        #验证数据
        if not all([mobile, imagecode, password, password2]):
            #验证手机号
            user = User.query.filter(User.phone == mobile).first()

            # 效验手机号是否合法
            if not re.match(r'^1[3456789]\d{9}$', mobile):
                return jsonify({'code':'1001','msg':'手机不对'})
            # # 效验验证码是否正确
            if session.get('code') != imagecode:
                return jsonify({'code':'1002','msg':'验证码不对'})

            # 效验用户是否已存在
            if user:
                return jsonify(status_code.USER_ERROR)
            if password != password2:
                return jsonify(status_code.USER_PASSWORD_ERROR)
            u = User()
            u.phone = mobile
            u.name = mobile
            u.password = password
            u.add_update()
            return jsonify({'code':200})





@user_blue.route('/login/',methods=['GET'])
def login():
    if request.method == 'GET':

        return render_template('login.html')


@user_blue.route('/login/', methods=['POST'])
def my_login():
    if request.method == 'POST':

        """
        登录验证
        """
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        # 效验信息完整
        if not all([password, mobile]):
            return jsonify(status_code.USER_NOT_ALL)
            # 效验手机号是否合法
        if not re.match(r'^1[3456789]\d{9}$', mobile):
            return jsonify(code='1003',msg='手机号格式不正确')
        user = User.query.filter(User.phone == mobile).first()
        # 效验用户是否存在
        if user:
            if user.check_pwd(password):
                # 效验密码是否正确
                session['user_id'] = user.id
                return jsonify({'code':'200','msg':'请求成功'})
            else:
                return jsonify(code='1002',msg='密码错误')
        else:
            return jsonify(code='1001',msg='该用户不存在')


#登录之后进入用户my
@user_blue.route('/my/',methods=['GET'])
@is_login
def my():

    return render_template('my.html')


@user_blue.route('/my_info/',methods=['GET'])
@is_login
def my_info():

    user = User.query.filter_by(id=session['user_id']).first()

    return jsonify(code=200,msg='请求成功',data=user.to_basic_dict())



@user_blue.route('/logout/',methods=['GET'])
@is_login
def logout():
    session.clear()
    return jsonify(code='200',msg='请求成功')



'''
修改用户信息
'''
@user_blue.route('/profile/', methods=['GET'])
@is_login
def profile():
    if request.method == 'GET':
        #跳转至修改用户信息界面
        return render_template('profile.html')


@user_blue.route('/profile/', methods=['PATCH'])
@is_login
def my_profile():
    """
    处理用户提出的修改请求
    """
    name = request.form.get('name')
    avatar = request.files.get('avatar')

    if avatar:
        try:
            # mime-type:表示文件的类型，如text/html,text/xml,image/png,image/jpeg..
            if not re.match('image/.*', avatar.mimetype):
                return jsonify(status_code.USER_PROFILE_IMAGE_UPDATE_ERROR)
        except:
            return jsonify(code=status_code.PARAMS_ERROR)

        # 项目路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 上传图片地址
        UPLOAD_FOLDER = os.path.join(os.path.join(BASE_DIR, 'static'), 'media')
        # 保存到media中
        filename = str(uuid.uuid4())
        a = avatar.mimetype.split('/')[-1:][0]
        file_name = filename +'.'+ a
        url = os.path.join(UPLOAD_FOLDER, file_name)
        avatar.save(url)
        # 保存用户的头像信息
        try:
            user = User.query.get(session['user_id'])
            user.avatar = os.path.join('/static/media', file_name)
            user.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)
        # 返回图片信息
        return jsonify(code='200', url=os.path.join('/static/media', avatar.filename))
    elif name:
        # 判断用户名是否存在
        if User.query.filter_by(name=name).count():
            return jsonify(status_code.USER_REGISTER_USER_IS_EXSITS)
        else:
            user = User.query.get(session['user_id'])
            user.name = name
            user.add_update()
            return jsonify(status_code.SUCCESS)
    else:
        return jsonify(status_code.PARAMS_ERROR)







'''
实名认证
'''
@user_blue.route('/auth/', methods=['GET'])
@is_login
def auth():
    return render_template('auth.html')



@user_blue.route('/auth_info/', methods=['GET'])
@is_login
def auth_info():
    # 获取当前登录用户的编号
    user_id = session['user_id']
    # 根据编号查询当前用户
    user = User.query.get(user_id)
    # 返回用户的真实姓名、身份证号
    return jsonify(user.to_auth_dict())



@user_blue.route('/auth/', methods=['POST'])
@is_login
def my_auth():
    id_name = request.form.get('real_name')
    id_card = request.form.get('id_card')

    # 验证参数完整性
    if not all([id_card, id_name]):
        return jsonify(status_code.PARAMS_ERROR)
    if not re.match('^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',id_card):
        return jsonify(status_code.USER_REGISTER_AUTH_ERROR)
    #修改数据对象
    try:
        user = User.query.get(session['user_id'])
    except:
        return jsonify(status_code.DATABASE_ERROR)

    try:
        user.id_card = id_card
        user.id_name = id_name
        user.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)
    # 返回数据
    return jsonify(status_code.SUCCESS)






