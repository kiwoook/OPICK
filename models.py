from enum import unique
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import redirect

db = SQLAlchemy()

class User(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'user_info' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)  #유저 이름
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.set_password(password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_username(self, username):
        return username