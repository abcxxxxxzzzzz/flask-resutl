from conf.db_base import BaseModel, db
from itsdangerous import BadSignature, SignatureExpired,TimedJSONWebSignatureSerializer 
from conf.config import BaseConfig
from passlib.apps import custom_app_context as pwd_context
from conf.config import BaseConfig
from utils.api_errors_code import ApiResponse


# 提供用户密码进行Token认证
class UserModel(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))

    # 基于 username 和 password 验证
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


    # 基于 Token 验证
    def generate_auth_token(self, expiration = 600):
        s = TimedJSONWebSignatureSerializer(BaseConfig.SECRET_KEY, expires_in = BaseConfig.EXPIRES_IN)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        '''Token 验证'''
        is_blacklisted_token = BlacklistToken.check_blacklist(token)
        if is_blacklisted_token:
                return None

        s = TimedJSONWebSignatureSerializer(BaseConfig.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired: # Expiration of token
            return None
        except BadSignature:
            return None         # Invalid token
        user = UserModel.query.get(data['id'])
        if not user:
            return None
        return user

    



class BlacklistToken(BaseModel):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)


    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True  
        else:
            return False