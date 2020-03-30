from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    student_id = Column(String(32), nullable=False, )
    student_name = Column(String(16), nullable=False)

    def set_attrs(self, form_dict):
        for key, value in form_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)


class AdminBaseModel(BaseModel):
    __abstract__ = True
    root = Column(String(16), nullable=False)
    root_name = Column(String(32), nullable=False)