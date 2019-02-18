
import functools
import redis

from flask import session
from werkzeug.utils import redirect



'''
装饰器（验证登录状态）
'''
def is_login(view_fun):
    @functools.wraps(view_fun)
    def decorator(*args,**kwargs):

        try:
            if 'user_id' in session:
                return view_fun(*args,**kwargs)
            else:
                return redirect('/user/login/')
        except Exception as e:
            print(e)
            return redirect('/user/login/')
    return decorator



