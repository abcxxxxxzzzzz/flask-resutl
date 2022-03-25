from functools import wraps
from flask import g
from models.user import UserModel
from conf.config import BaseConfig
from flask import request
from utils.api_errors_code import ApiResponse

# from flask_httpauth import HTTPBasicAuth
# auth = HTTPBasicAuth()


# 自定义全局认证装饰器
def authenticate():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            auth = verify_token()
            if auth:
                return fn(*args, **kwargs)
            else:
                return ApiResponse.AuthFailed()
        return decorator
    return wrapper

# 获取 Token 
def get_header_token():
    auth_header = request.headers.get(BaseConfig.AUTH_HEADER_NAME)
    if auth_header:
        auth_token = auth_header
    else:
        auth_token = ''
    return auth_token



# 一种基于 Token
# @auth.verify_password                              # 定义校验密码的回调函数
def verify_token():    
    
    """从头部获取 token """
    auth_token = get_header_token()
    # 先验证 Token 是否有效，如果Token无效或者没有Token,则验证用户密码
    user = UserModel.verify_auth_token(auth_token)
    if not user:
        return False
    g.user = user                                   # 全局变量                           
    return True                                     # 校验通过返回True





