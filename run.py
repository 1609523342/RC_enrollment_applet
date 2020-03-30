#-- coding: UTF-8 --
from app import creat_app
import json
from app.models.Application_model import SuperUser
from app.models.Base_model import db
from app.forms.error_code import Success, SQLException
from flask import jsonify


app = creat_app()


@app.route('/superadmin/', methods=['POST'])
def creat_super():
    data = SuperUser.query.filter(SuperUser.account =='super_admins').first()
    try:
        if not data:
            superuser = SuperUser(root='2', root_name='6', account='super_admins',
                                   password='Superadministrator', student_id='无', student_name='无')
            db.session.add(superuser)
            db.session.commit()
            return Success()
    except:
        raise SQLException()
    else:
        return jsonify('该用户已存在,不可再创建')


@app.route('/hello')
def hello():
    headers = {
        'Content-Type': 'application/json'
    }
    data = {'openid': '201810098030', 'session_key': 'key'}
    datas = json.dumps(data)
    return datas, 200, headers


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
