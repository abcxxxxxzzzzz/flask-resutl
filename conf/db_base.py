from contextlib import contextmanager
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

# 封装 SQL 提交和 回滚
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True  ## 声明当前类为抽象类，被继承，调用不会被创建
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_by = db.Column(db.String(64), comment="创建者")
    created_at = db.Column(db.TIMESTAMP(True), comment="创建时间", nullable=False, server_default=func.now())
    update_by = db.Column(db.String(64), comment="更新者")
    updated_at = db.Column(db.TIMESTAMP(True), comment="更新时间", nullable=False, server_default=func.now(),
                           onupdate=func.now())
    remark = db.Column(db.String(500), comment="备注")

    def save(self):
        '''
        新增数据
        :return:
        '''
        db.session.add(self)


    def update(self):
        '''
        更新数据
        :return:
        '''
        db.session.merge(self)


    def delete(self):
        '''
        删除数据
        :return:
        '''
        db.session.delete(self)


    def save_all(self, data):
        '''
        保存多条数据
        :param data:
        :return:
        '''
        db.session.execute(
            self.__table__.insert(),
            data
        )
