from multiprocessing import synchronize
from flask_restful import Resource, reqparse, marshal, marshal_with, marshal_with_field, fields
from utils.authentication import authenticate
from utils.api_errors_code import ApiResponse
from models.user import UserModel
from sqlalchemy import or_



user_fields = {
    'id': fields.Integer,
    'username': fields.String,
}

class UserListAPI(Resource):
    """用户信息"""

    decorators = [authenticate()]

    def __init__(self):
        """ 资源验证 """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('search', type = str, required = False, location = 'args', trim=True, default = None)            # 分页页码, 默认为None
        self.reqparse.add_argument('page', type = int, required = False, location = 'args',default = 1)            # 分页页码, 默认为1，
        self.reqparse.add_argument('page_size', type = int,required = False, location = 'args',default = 20)    # 分页显示数量，可选 choices() 规定只能用几个数量
        #  choices=(50,100,200,500),
        super(UserListAPI, self).__init__()

    def get(self):
        '''查询'''
        """
        获取所有信息
        search： 如果存在搜索内容，搜索后分页，支持批量搜索，格式： http://10.11.9.246:8000/api/v1.0/users?page=1&page_size=2&search=admin2,admin3,admin
        page: 请求页
        page_size: 当前页面数量
        """
        args = self.reqparse.parse_args()
        search = args.get('search')
        page = args.get('page')
        page_size = args.get('page_size')


        if search and len(search.split(',')) > 0:        
            OR_ = or_( UserModel.username == s.replace(' ','') for s in search.split(','))
            obj = UserModel.query.filter(OR_)
            users = obj.paginate(page, page_size)
        else:
            users = UserModel.query.paginate(page, page_size)

        # users = UserModel.query.limit(page_size).offset((page-1) * page_size).all()
        
        return ApiResponse.SUCCESS(
                data = marshal(users.items, user_fields), 
                total = users.total,
                current_page = users.page,
                total_pages = users.pages
            )


    def post(self):
        """ 添加 """
        self.reqparse.add_argument('username', type = str, required = True, location = 'json',help = 'Username Required')
        self.reqparse.add_argument('password', type = str, required = True, location = 'json',help = 'Username Required')
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']

        if len(username)  == 0 or len(password) == 0:
            return ApiResponse.ClientTypeError()

        if UserModel.query.filter_by(username = username).first() is not None:
            return ApiResponse.ParameterException(msg='{} Already exists'.format(username))

        user = UserModel(username = username)
        user.hash_password(password)
        user.save()
        return ApiResponse.SUCCESS(marshal(user, user_fields))


class UserAPI(Resource):
    

    decorators = [authenticate()]

    def __init__(self):
        """ 资源验证 """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('password', type = str, required = True, location = 'json')
        super(UserAPI, self).__init__()

    def get(self, id):
        """获取单条数据"""
        user = UserModel.query.get_or_404(id)
        if user:
            return ApiResponse.SUCCESS(marshal(user, user_fields))
        return ApiResponse.NotFoudError()

    def put(self, id):
        """更新单条数据"""
        args = self.reqparse.parse_args()
        password = args['password']
        user = UserModel.query.get(id)
        if user:
            user.hash_password(password)
            user.update()
            return ApiResponse.SUCCESS()
        return ApiResponse.NotFoudError()
        
    def delete(self, id):
        user = UserModel.query.get_or_404(id)
        if user:
            user.delete()
            return ApiResponse.SUCCESS()
        return ApiResponse.NotFoudError()




class BatchAPI(Resource):

    def __init__(self):
        """ 资源验证 """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('batch', type = list, required = True, location = 'json')
        super(BatchAPI, self).__init__()

    def post(self):
        '''批量增'''
        args = self.reqparse.parse_args()
        batch = args['batch']
        print(batch) # [{'username': 'admin5', 'password': '123456'}, {'username': 'admin6', 'password': '123456'}]
        # 由于我这里牵涉到密码加密，调用加密是写死的，只能 for 循环添加，如果其他数据，直接传进来，调用 save_all(data) 即可
        # 实现批量新增数据
        # db是sqlalchemy对象，ExamSchool是通过db.Modal创建的数据表，虽然也是循环新增，不过效率快多了
        # db.session.execute(ExamSchool.__table__.insert(),
        # 	 [{"eid": int(form.get('id')), "sid": int(i)} for i in new_schools]
        # )

        return ApiResponse.SUCCESS()

    def put(self):
        '''批量改'''
        # ExamSchool 与 exam 是一对多关系, 其他的循环修改，或者 filter_by(or_(xx=xx, xx=xx))
        # db.session.query(ExamSchool).filter(ExamSchool.eid == exam.id). \
        #         update({ExamSchool.status: 0}, synchronize_session=False)

        # 类似下面删除： 通过ID查询出来，再更新， UserModel.query.filter(UserModel.id.in_(ids)).update(xxx=xxx)

        pass

    def delete(self):
        '''批量删'''
        # ExamSchool 与 exam 是一对多关系
        # db.session.query(ExamSchool).filter(ExamSchool.eid == exam.id).delete()

        # 通过 ID 删除
        # ids = ids.split(",")       # 传入字符串，或者删除的id列表
        # users = UserModel.query.filter(UserModel.id.in_(ids)).all()
        # [db.session.delete(u) for u in users]
        ids = '3,4'
        ids = ids.split(",") 
        UserModel.query.filter(UserModel.id.in_(ids)).delete(synchronize_session=False)
        return ApiResponse.SUCCESS()