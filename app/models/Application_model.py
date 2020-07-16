from sqlalchemy import Column, Integer, String
from werkzeug.security import check_password_hash
from app.models.Base_model import BaseModel, AdminBaseModel
from werkzeug.security import generate_password_hash
from app.models.Base_model import db

class message(BaseModel):
    __abstract__ = False
    id = Column(Integer, primary_key=True, autoincrement=True)
    sex = Column(String(4), nullable=False)
    birth = Column(String(16), nullable=False)
    grade = Column(String(16), nullable=False)
    major = Column(String(32), nullable=False)
    classes = Column(String(16), nullable=False)
    post = Column(String(16), nullable=False)
    other_organization = Column(String(64), nullable=False)
    Speciality = Column(String(64), nullable=False)
    QQ = Column(String(32))
    email = Column(String(32))
    phone_number = Column(String(32), nullable=False)
    short_phone = Column(String(16))
    first_choice = Column(String(16), nullable=False)
    second_choice = Column(String(16), nullable=False)
    Compliance_or_not = Column(String(16), nullable=False)
    Personal_profile = Column(String(256), nullable=False)
    Ideas_and_creativity = Column(String(256), nullable=False)
    photo_url = Column(String(256))
    Purpose_of_joining = Column(String(256), nullable=False)
    Submission_time = Column(String(64), nullable=False)


class User(AdminBaseModel):
    __abstract__ = False
    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(32), nullable=False)


class SuperUser(AdminBaseModel):
    __abstract__ = False
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(12), nullable=False, unique=True)
    _password = Column('password', String(128), nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, key):
        self._password = generate_password_hash(key)

    def check_password(self, key):
        return check_password_hash(self._password, key)


class SwitchList(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(12), nullable=False, unique=True)


