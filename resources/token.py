import json
from flask_restful import Resource,reqparse
from utils.authentication import get_header_token
from models.user import BlacklistToken, UserModel
from flask import g, jsonify
from utils.authentication import authenticate
from utils.api_errors_code import ApiResponse

class LoginApi(Resource):

    '''登录'''

    def __init__(self):
        """ 资源验证 """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True, location = 'json')
        self.reqparse.add_argument('password', type = str, required = True, location = 'json')
        super(LoginApi, self).__init__()


    # 登录返回token
    def post(self):
        """

        @@@
        ### data
        |  data | nullable | request type | type |  remarks |
        |-------|----------|--------------|------|----------|
        | username |  false   |  body     | json  | 用户名字    |
        | password  |  false   | body     | json  | 用户密码 |

        ### request
        ```json
        {"username": "xxx", "password": "xxx"}
        ```

        ### return
        ```json
        {
            "code": 200,
            "data": {
                "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTY0ODE4NjkzNCwiZXhwIjoxNjQ4MTk2OTMzfQ.eyJpZCI6MX0.NmOU1LE-LkcXNLM5CfZ5l8I5WR-d1M797AUh7hUWFekFnNyLBJFgP55QldPIMUtN3AVcBSMG_k_DxB5SVhZ--A"
            },
            "msg": "ok"
        }
        ```
        @@@
        """
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']
        user = UserModel.query.filter_by(username = username).first()
        if not user or not user.verify_password(password):
            return ApiResponse.AuthFailed()
        auth_token = user.generate_auth_token()
        return ApiResponse.SUCCESS(data={'token': auth_token.decode('ascii')})



    

class LogoutApi(Resource):

    '''退出'''

    decorators = [authenticate()]

    # 退出，token加入黑名单，实现过期
    def delete(self):
        '''
        @@@
        ## 示例
        ```python
        import requests

        url = "http://127.0.0.1:8000/api/v1.0/auth/logout"

        payload={}
        headers = {
        'X-Token': 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY0ODE4MzY4MiwiZXhwIjoxNjQ4MTkzNjgxfQ.eyJpZCI6MX0.LUnBmqfZFDl2s4lHJGUFpPEuDMp9JNDdhK6ARY7rHBMYcfiQTV2YMtOu3oDRj03Sc9HsaGo-MIxpX0jnoo03lQ'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text)

        ```

        ```bash
        curl --location --request DELETE 'http://127.0.0.1:8000/api/v1.0/auth/logout' \
        --header 'X-Token: <you-token>'
        ```
        @@@
        
        '''
        auth_token = get_header_token()
        if auth_token:
            user = UserModel.verify_auth_token(auth_token)
            if user:
                blacklist_token = BlacklistToken(token=auth_token)
                blacklist_token.save()
                return ApiResponse.SUCCESS()
            else:
                return ApiResponse.AuthFailed()
        else:
            return ApiResponse.AuthFailed()