OK = 200
SUCCESS = {'code': 200, 'msg': '请求成功'}
PARAMS_ERROR = {'code': 400, 'msg': '参数错误'}
DATABASE_ERROR = {'code': 500, 'msg': '内部错误'}

# 用户模块
USER_NOT_ALL = {'code': 1000, 'msg': '参数不完整'}
USER_MOBILE_ERROR = {'code': 1001, 'msg': '非法手机号'}
USER_IMAGECODE_ERROR = {'code': 1002, 'msg': '验证码错误'}
USER_PASSWORD_ERROR = {'code': 1003, 'msg': '密码不一致'}
USER_ERROR = {'code': 1004, 'msg': '用户已存在'}


USER_PROFILE_IMAGE_UPDATE_ERROR = {'code': 1005, 'msg': '文件类型错误'}
USER_REGISTER_USER_IS_EXSITS = {'code': 1006, 'msg': '用户名已存在'}
USER_REGISTER_AUTH_ERROR = {'code': 1007, 'msg': '身份证号码错误'}

# 房屋信息
MYHOUSE_USER_IS_NOT_AUTH = {'code': 1008, 'msg': '该用户未实名认证'}

# 房屋出租
ORDER_START_END_TIME_ERROR = {'code': 10009, 'msg': '该房屋已被其它客户租住'}
