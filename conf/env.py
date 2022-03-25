# ================================
# MYSQL 数据库相关
# ================================
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'AAbb1122..'
MYSQL_DATABSE = 'devops'


# ================================
# REDIS 相关
# ================================
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_DB = 0
REDIS_EXPIRE = 6000


# ===============================
# DEBUG 
# ================================
DEBUG = True
API_VERSION = 'v1.0'


# ===============================
# 日志级别、存放日志目录 
# ================================
LOG_LEVEL = "DEBUG"
LOG_DIR_NAME = "logs"



# ===============================
# 是否生成 API 文档，如果生成则改为 True,不生成该为False, api登录用户
# 参考地址： https://github.com/kwkwc/flask-docs
# ================================
API_DOC_ENABLE = True
API_DOC_LOGIN_NAME = 'admin'
API_DOC_URL_PREFIX = '/docs/api'
API_DOC_TITLE = "Restful API 文档"
API_DOC_VERSION = API_VERSION
API_DOC_DESCRIPTION = "flask-restful api 生成文档"