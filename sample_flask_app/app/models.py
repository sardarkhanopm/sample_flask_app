from . import db


class LongRunningTask(db.Model):
    task_id = db.Column(db.String(50), primary_key=True)
    status = db.Column(db.String(25))
    output = db.Column(db.Text(2000))

    @property
    def to_dict_without_output(self) -> dict:
        result_dict = {}
        for column in self.__table__.columns:
            if column.name != 'output':
                result_dict[column.name] = getattr(self, column.name)
        return result_dict

    @property
    def to_dict(self) -> dict:
        result_dict = {}
        for column in self.__table__.columns:
            result_dict[column.name] = getattr(self, column.name)
        return result_dict


class SnowFlakeConnection(db.Model):
    connection_name = db.Column(db.String(20), unique=True, primary_key=True)
    account_name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    @property
    def to_dict_without_password(self) -> dict:
        result_dict = {}
        for column in self.__table__.columns:
            if column.name != 'password':
                result_dict[column.name] = getattr(self, column.name)
        return result_dict
