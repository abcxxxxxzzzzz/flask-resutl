from flask import Flask
from routes.routes import api_bp
from .config import config, handler
from .db_base import db
from . import env


# 生成 API 文档
def init_api_doc(app):
    from flask_docs import ApiDoc
    api_doc = ApiDoc(
        app,
        title=env.API_DOC_TITLE,
        version=env.API_DOC_VERSION,
        description=env.API_DOC_DESCRIPTION
    )

    return api_doc


# 传值 config_name, 设定运行环境(开发，测试，生产) 
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app=app)


    # 加载 API 文档
    init_api_doc(app)

    # 加载数据库
    # with app.app_context():
    db.init_app(app=app)
    

    # 加载日志
    app.logger.addHandler(handler)

    # 注册使用flask_restful框架的路由
    app.register_blueprint(api_bp)


    return app


