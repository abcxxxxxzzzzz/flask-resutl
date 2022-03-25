from flask import Blueprint
from flask_restful import Api
from resources.user import UserAPI, UserListAPI, BatchAPI
from resources.token import LoginApi, LogoutApi
from conf import env


API_VERSION_URL = '/api/' + env.API_VERSION



# 重写 handle_error（）函数, 交给全局异常处理
class RewriteApi(Api):
    def handle_error(self, e):
        raise e

# Blueprint('蓝图名字', import_name, 规则前缀)
api_bp = Blueprint('tasks', __name__,url_prefix=API_VERSION_URL)
api = RewriteApi(api_bp)




# Auth 路由
api.add_resource(LoginApi, '/auth/login', endpoint= 'login')        # 用户登录,返回 token
api.add_resource(LogoutApi, '/auth/logout', endpoint= 'logout')     # 用户退出, Token 加入黑名单



# Users 路由
api.add_resource(UserListAPI, '/users', endpoint = 'users')      # [查询，批量查询，分页，添加用户]
api.add_resource(UserAPI, '/user/<int:id>', endpoint = 'user')   # 单个用户删、改、查


api.add_resource(BatchAPI, '/users/batch', endpoint='users_batch')


