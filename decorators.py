## 此装饰器为 仅需要登录才能使用的页面服务
from functools import wraps

from flask import redirect, url_for, g


def log_required(func):
    @wraps(func)
    def inner(*arg,**kwargs):
        if g.user:
            return func(*arg,**kwargs)
        else:
            return redirect(url_for("auth.log"))
    return inner