from wtforms import Form

from app.forms.error_code import ParameterException


class BaseForm(Form):
    def __init__(self, data):
        super(BaseForm, self).__init__(data=data)

    def validate_error_message(self):
        message = super(BaseForm, self).validate()
        if not message:
            raise ParameterException(msg=self.errors)

