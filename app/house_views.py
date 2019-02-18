import os

from flask import render_template, request, session, jsonify

from app.models import User, House, Area, Facility, HouseImage, Order
from app.user_views import Blueprint
from utils import status_code
from utils.funtions import is_login

house_blue = Blueprint('house',__name__)

#首页
@house_blue.route('/index/',methods=['GET'])
def index():
    if request.method == 'GET':

        return render_template('index.html')


@house_blue.route('/index_info/',methods=['GET'])
def index_info():
    # 获取最新的3个房屋信息
    hlist = House.query.order_by(House.id.desc()).all()[:3]
    hlist2 = []
    for house in hlist:
        hlist2.append(house.to_dict())

    # 查找地区信息
    area_list = Area.query.all()

    area_dict_list = [area.to_dict() for area in area_list]
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        user_name = user.name
        code = status_code.OK
        return jsonify(code=code, name=user_name, hlist=hlist2, alist=area_dict_list)
    return jsonify(code=200, hlist=hlist2,alist=area_dict_list)






# 搜索
@house_blue.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@house_blue.route('/my_search/', methods=['GET'])
def my_search():
    # 先获取区域id，订单开始时间，结束时间
    aid = request.args.get('aid')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    sk = request.args.get('sk')
    # 获取某个区域的房屋信息
    houses = House.query.filter(House.area_id == aid)
    # 订单的三种情况，查询出的房屋都不能展示
    order1 = Order.query.filter(Order.end_date >= ed, Order.begin_date <= ed)
    order2 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= sd)
    order3 = Order.query.filter(Order.begin_date >= sd, Order.end_date <= ed)
    house1 = [order.house_id for order in order1]
    house2 = [order.house_id for order in order2]
    house3 = [order.house_id for order in order3]
    # 去重
    not_show_house_id = list(set(house1 + house2 + house3))
    # 最终展示的房屋信息
    houses = houses.filter(House.id.notin_(not_show_house_id))
    # 排序
    if sk == 'new':
        houses = houses.order_by('-id')
    elif sk == 'booking':
        houses = houses.order_by('-order_count')
    elif sk == 'price-inc':
        houses = houses.order_by('price')
    elif sk == 'price-des':
        houses = houses.order_by('-price')

    house_info = [house.to_dict() for house in houses]
    return jsonify(code=status_code.OK, house_info=house_info)




'''
我的房源
'''
@house_blue.route('/myhouse/', methods=['GET'])
@is_login
def myhouse():
    return render_template('myhouse.html')


@house_blue.route('/my_house/', methods=['POST'])
@is_login
def my_house():
    #验证当前用户是否完成实名认证
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user.id_name:
        #如果已完成实名认证，则查询当前用户的房源信息
        house_list = House.query.filter(House.user_id == user_id).order_by(House.id.desc())
        house_list2 = []
        for house in house_list:
            house_list2.append(house.to_dict())
        return jsonify(code=200,hlist=house_list2)

    else:
        return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


@house_blue.route('/area_facility/', methods=['GET'])
@is_login
def area_facility():
    #查询地址
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]
    #查询设施
    facility_list = Facility.query.all()
    facility_dict_list = [facility.to_dict() for facility in facility_list]
    #构造结果并返回数据
    return jsonify(area=area_dict_list,facility=facility_dict_list)


'''
发布房源
'''
@house_blue.route('/newhouse/', methods=['GET'])
@is_login
def newhouse():
    return render_template('newhouse.html')



@house_blue.route('/new_house/', methods=['POST'])
@is_login
def new_house():
    #接收用户信息
    params = request.form.to_dict()
    facility_ids = request.form.getlist('facility')

    #创建房源信息
    house = House()
    house.user_id = session['user_id']
    house.area_id = params.get('area_id')
    house.title = params.get('title')
    house.price = params.get('price')
    house.address = params.get('address')
    house.room_count = params.get('room_count')
    house.acreage = params.get('acreage')
    house.beds = params.get('beds')
    house.unit = params.get('unit')
    house.capacity = params.get('capacity')
    house.deposit = params.get('deposit')
    house.min_days = params.get('min_days')
    house.max_days = params.get('max_days')
    #通过设施编号查询设施对象
    if facility_ids:
        facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facility_list
    house.add_update()
    return jsonify(code=200,house_id=house.id)


#接收发布房源图片
@house_blue.route('/image_house/', methods=['POST'])
@is_login
def image_house():
    #接收房屋编号
    house_id = request.form.get('house_id')
    #接收图片
    h_image = request.files.get('house_image')
    #保存图片到images
    # 项目路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 上传图片地址
    UPLOAD_FOLDER = os.path.join(os.path.join(BASE_DIR, 'static'), 'images')
    url = os.path.join(UPLOAD_FOLDER, h_image.filename)
    h_image.save(url)
    #保存到数据库
    image = HouseImage()
    image.house_id = house_id
    image.url = os.path.join('/static/images', h_image.filename)
    image.add_update()

    #首图
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = os.path.join('/static/images', h_image.filename)
        house.add_update()

    return jsonify(code=200,url=os.path.join('/static/images', h_image.filename))


#房源信息
@house_blue.route('/detail/')
@is_login
def detail():

    return render_template('detail.html')


@house_blue.route('/house_detail/',methods=['GET'])
@is_login
def house_detail():
    #获取房屋信息
    house_id = request.args.get('house_id')
    house = House.query.get(house_id)
    #获取设施信息
    facility_list = house.facilities
    facility_dict_list = [facility.to_dict() for facility in facility_list]
    # 判断当前房屋信息是否为当前登录的用户发布，如果是则不显示预订按钮
    booking = 1
    if 'user_id' in session:
        if house.user_id == session['user_id']:
            booking = 0

    return jsonify(code=200,house=house.to_full_dict(),facility_list=facility_dict_list,booking=booking)


@house_blue.route('/booking/')
@is_login
def booking():
    return render_template('booking.html')


@house_blue.route('/house_booking/',methods=['GET'])
@is_login
def house_booking():
    # 获取房屋信息
    id = request.args.get('house_id')
    house = House.query.get(id)
    return jsonify(code=200,house=house.to_dict())

