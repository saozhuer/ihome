import os

from flask import render_template, request, session, jsonify
from datetime import datetime
from app.models import User, House, Area, Facility, HouseImage, Order
from app.user_views import Blueprint
from utils import status_code
from utils.funtions import is_login

order_blue = Blueprint('order',__name__)


#个人订单
@order_blue.route('/my_order/', methods=['GET'])
def my_order():
    if request.method == 'GET':
        return render_template('orders.html')


@order_blue.route('/my_order/', methods=['POST'])
def order():
    #获取评价
    comment = request.form.get('comment')
    order_id = request.form.get('order_id')
    print(order_id)
    #存入数据库
    order = Order.query.filter_by(id=order_id).first()
    order.comment = comment
    order.add_update()
    return jsonify(code=200)



@order_blue.route('/create_order/',methods=['POST'])
@is_login
def create_order():
    #获取参数
    dict = request.form
    house_id = int(dict.get('hosue_id'))

    start_date = datetime.strptime(dict.get('begin_date'),'%Y-%m-%d')
    end_date = datetime.strptime(dict.get('end_date'),'%Y-%m-%d')
    # 验证有效性
    if not all([house_id, start_date, end_date]):
        return jsonify(status_code.PARAMS_ERROR)
    if start_date > end_date:
        return jsonify(status_code.ORDER_START_END_TIME_ERROR)
    #获取房屋对象
    house = House.query.get(house_id)

    #创建订单对象
    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = (end_date - start_date).days +1
    order.house_price = house.price
    order.amount = order.house_price * order.days

    try:
        order.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify(code=200,msg='请求成功')




#我的订单
@order_blue.route('/all_orders/', methods=['GET'])
@is_login
def all_orders():
    uid = session['user_id']
    order_list = Order.query.filter(Order.user_id == uid).order_by(Order.id.desc())
    # order_list2 = [order.to_dict() for order in order_list]
    order_list2 = []
    for order in order_list:
        for status in [('WAIT_ACCEPT','待接单'),('WAIT_PAYMENT','待支付'),('PAID','已支付'),('WAIT_COMMENT','待评价'),
                      ('COMPLETE','已完成'),('CANCELED','已取消'),('REJECTED','已拒单')]:
            if status[0] == order.status:
                dict = order.to_dict()
                dict['status'] = status[1]
                break
        order_list2.append(dict)

    return jsonify(code=200,all_orders=order_list2)


#客户订单
@order_blue.route('/lorders/', methods=['GET'])
@is_login
def lorders():
    return render_template('lorders.html')


@order_blue.route('/my_lorders/', methods=['GET'])
@is_login
def my_lorders():
    #获取订单信息
    uid = session['user_id']
    # 查询当前用户的所有房屋编号
    hlist = House.query.filter(House.user_id == uid)
    hid_list = [house.id for house in hlist]
    # 根据房屋编号查找订单
    order_list = Order.query.filter(Order.house_id.in_(hid_list)).order_by(Order.id.desc())
    # 构造结果
    olist=[]
    for order in order_list:
        for status in [('WAIT_ACCEPT','待接单'),('WAIT_PAYMENT','待支付'),('PAID','已支付'),('WAIT_COMMENT','待评价'),
                      ('COMPLETE','已完成'),('CANCELED','已取消'),('REJECTED','已拒单')]:
            if status[0] == order.status:
                dict = order.to_dict()
                dict['status'] = status[1]
                break
        olist.append(dict)


    return jsonify(olist=olist)



'''
修改订单状态
'''
@order_blue.route('/orders_status/',methods=['POST'])
def status():
    #接收参数：状态
    order_status=request.form.get('orders_status')

    for status in [('WAIT_ACCEPT', '待接单'), ('WAIT_PAYMENT', '待支付'), ('PAID', '已支付'), ('WAIT_COMMENT', '待评价'),
                   ('COMPLETE', '已完成'), ('CANCELED', '已取消'), ('REJECTED', '已拒单')]:
        if order_status == status[1]:
            order_status = status[0]
            break

    #查找订单对象
    id = request.form.get('order_id')
    order=Order.query.get(id)
    #修改
    order.status=order_status
    #如果是拒单，需要添加原因
    if order_status=='REJECTED':
        order.comment=request.form.get('comment')
    #保存
    try:
        order.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)

    return jsonify(code=status_code.OK)