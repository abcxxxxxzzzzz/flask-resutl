
from conf import create_app
from werkzeug.exceptions import HTTPException
from utils.api_errors_base import APIException
from flask_migrate import Migrate, MigrateCommand
from flask_script import Server, Manager
from conf.db_base import db

# from conf.db_base import db
# from conf import  create_app
# db.create_all(app=create_app('default'))







app = create_app("default")



@app.errorhandler(Exception)
def framework_error(e):

    # 判断异常是不是APIException
    if isinstance(e, APIException):
        return e
    # 判断异常是不是HTTPException
    if isinstance(e, HTTPException):
        code = e.code
        # 获取具体的响应错误信息
        msg = e.description
        error_code = 1007
        return APIException(code=code, msg=msg, error_code=error_code)
    # 异常肯定是Exception
    else:
        # 如果是调试模式,则返回e的具体异常信息。否则返回json格式的 APIException 对象！
        # 针对于异常信息，我们最好用日志的方式记录下来。
        if app.config["DEBUG"]:
            return APIException()
        raise e
 



manager = Manager(app)
Migrate(app=app, db=db)

manager.add_command('db', MigrateCommand) # 创建数据库映射命令
manager.add_command('start', Server(host='0.0.0.0',port=8000)) # 创建启动命令



if __name__ == '__main__':
    
    # app.run(host='0.0.0.0',port=8000)
    manager.run()