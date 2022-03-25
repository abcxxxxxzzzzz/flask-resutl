from .api_errors_base import APIException
from flask import jsonify
import enum

class Code(enum.Enum):
    # 请求状态吗
    SUCCESS = 200
    BADREQUEST_CODE = 400       # 客户端类型错误
    SERVER_CODE = 500                # 服务器内部错误
    AUTHFAILED = 401
    NOTFOUDERROR = 404
    
    

class ApiResponse(APIException):

    def SUCCESS(data=None, *args, **kwargs):
        return jsonify(code=Code.SUCCESS.value, msg="ok", data=data, *args, **kwargs)

    def ServerError(msg="Server is invallid!", data=None):
            return jsonify(code=Code.SERVER_CODE.value,error_code=999, msg=msg, data=data)

    def ClientTypeError(msg="Parameter is invallid!", data=None):
            return jsonify(code=Code.BADREQUEST_CODE.value,error_code=1001, msg=msg, data=data)

    def ParameterException(msg="Parameter is invallid!", data=None):
            return jsonify(code=Code.BADREQUEST_CODE.value,error_code=1002, msg=msg, data=data)

    def AuthFailed(msg="Authentication error!", data=None):
            return jsonify(code=Code.AUTHFAILED.value,error_code=1003, msg=msg, data=data)

    def NotFoudError(msg="Not found!", data=None):
            return jsonify(code=Code.NOTFOUDERROR.value,error_code=1004, msg=msg, data=data)




