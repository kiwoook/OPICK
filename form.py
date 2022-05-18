from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo
from models import User

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self,form,field):
            email = form['email'].data
            pw = field.data
            userinfo = User.query.filter_by(email=email).first()
            if(userinfo is None):
                raise ValueError('존재하지 않는 아이디입니다.')
            else :
                if userinfo.check_password(pw):
                    pass
                else:
                    raise ValueError('비밀번호 틀림')
        
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])             
    