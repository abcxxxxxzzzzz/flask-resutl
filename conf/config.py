import imp
from . import env
import os
import time
import logging
from utils.api_docs_sha256 import encryption



class BaseConfig:
    SECRET_KEY = "\xf9'\xe4p(\xa9\x12\x1a!\x94\x8d\x1c\x99l\xc7\xb7e\xc7c\x86\x02MJ\xa0"
    EXPIRES_IN = 9999                       # 令牌有效时间
    AUTH_HEADER_NAME = 'X-Token'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    # API 文档相关，默认显示所有
    API_DOC_ENABLE = env.API_DOC_ENABLE  # 是否启用 API 文档页面
    API_DOC_CDN = False      # 使用 CDN
    API_DOC_URL_PREFIX = env.API_DOC_URL_PREFIX        # 自定义 url_prefix
    API_DOC_PASSWORD_SHA2 = encryption(env.API_DOC_LOGIN_NAME)
    #API_DOC_METHODS_LIST = ["GET", "POST", "PUT", "DELETE", "PATCH"]    # 允许显示的方法
    #API_DOC_RESTFUL_EXCLUDE = ['xxxx']      # 需要排除的 RESTful Api 类名
    #API_DOC_MEMBER = ["xxx", "xxx"]         # 需要显示的 Api 蓝图名称
    #API_DOC_MEMBER_SUB_EXCLUDE = ['xxx']    # 需要排除的子成员 Api 函数名称
    

    @staticmethod
    def init_app(app):
        pass


# 开发环境
class DevelopmentConfig(BaseConfig):
    DEBUG = env.DEBUG
    base_dir = os.path.abspath(os.path.dirname(__file__))
    print(base_dir)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite') # 其中 db.sqlite 是为数据库添加的名字

    # DEBUG = env.DEBUG
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(env.MYSQL_USERNAME,
    #                                                                 env.MYSQL_PASSWORD,
    #                                                                 env.MYSQL_HOST, env.MYSQL_PORT,env.MYSQL_DATABSE)
# 测试环境
class TestingConfig(BaseConfig):
    TESTING = env.DEBUG
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(env.MYSQL_USERNAME,
                                                                   env.MYSQL_PASSWORD,
                                                                   env.MYSQL_HOST, env.MYSQL_PORT,env.MYSQL_DATABSE)

# 生成环境
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(env.MYSQL_USERNAME,
                                                                   env.MYSQL_PASSWORD,
                                                                   env.MYSQL_HOST, env.MYSQL_PORT,env.MYSQL_DATABSE)


# 引入时读取此配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'JSON_AS_ASCII': False
}
# 解决中文编码的问题
config.update(RESTFUL_JSON=dict(ensure_ascii=False))


# swagger_config = {
#     "headers": [
#         ],
#         "specs": [
#             {
#                 "endpoint": 'apispec_2',
#                 "route": '/apispecification.json',
#                 "rule_filter": lambda rule: True,  # all in
#                 "model_filter": lambda tag: True,  # all in
#             }
#         ],
#     "static_url_path": "/flasgger_static",
#     # "static_folder": "static",  # must be set by user
#     "swagger_ui": True,
#     "specs_route": "/doc/"
# }
# template_config = {
#   "info": {
#     "title": "Sample API",
#     "description": "Hahaha, this is a API kingdom!",
#     "version": "1.0.0"
#   }
# }
# ===================================
#  日志封装
# ====================================


# # 上传文件
# UPLOAD_HEAD_FOLDER = "static/uploads/avatar"
# app_url = "http://localhost:5000"



def make_dir(make_dir_path):
    """
    文件生成
    :param make_dir_path:
    :return:
    """
    path = make_dir_path.strip()
    if not os.path.exists(path):
        os.makedirs(path)
    return path


log_dir_name = env.LOG_DIR_NAME  # 日志文件夹
log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'  # 文件名
log_file_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + os.sep + log_dir_name
make_dir(log_file_folder)

log_file_str = log_file_folder + os.sep + log_file_name  # 输出格式
log_level = env.LOG_LEVEL  # 日志等级

handler = logging.FileHandler(log_file_str, encoding='UTF-8')
handler.setLevel(log_level)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)