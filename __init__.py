import os #디렉토리 절대 경로
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask import session #세션
from flask_wtf.csrf import CSRFProtect #csrf
from models import db
from models import User
from form import RegisterForm, LoginForm
from rank_crawling import ranking


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def mainpage():
    email = session.get('email', None)
    if(email != None):
        userinfo = User.query.filter_by(email=email).first()
        username = userinfo.username
        session['username'] = username
        return render_template('index.html',username=username,email=email)
    return render_template('index.html',email=email)
    
@app.route('/welcome')
def welcome(): 
    username = request.args.get('username')
    return render_template('welcome.html', username = username)

@app.route('/register', methods=['GET','POST']) #GET(정보보기), POST(정보수정) 메서드 허용
def register():
    register_form = RegisterForm()
    login_form = None
    if register_form.validate_on_submit(): #내용 채우지 않은 항목이 있는지까지 체크

        username =register_form.data.get('username')
        email =register_form.data.get('email')
        password =register_form.data.get('password')
        userinfo = User(email, username, password)
        db.session.add(userinfo) #DB저장
        db.session.commit() #변동사항 반영

        session['email'] = email
        return redirect(url_for('welcome', username = str(username)))
    return render_template('register.html', register_form=register_form , login_form = login_form)

@app.route('/login', methods=['GET','POST'])  
def login():
    
    login_form = LoginForm() #로그인폼
    register_form = RegisterForm()
    if login_form.validate_on_submit(): #유효성 검사
                    # print('{}가 로그인 했습니다'.format(form.data.get('username')))
        session['email']=login_form.data.get('email') #form에서 가져온 userid를 세션에 저장
        return redirect('/') #성공하면 main.html로
    return render_template('login.html', login_form = login_form, register_form = register_form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return redirect('/')

@app.route('/ranking/<int:ott>')
def rank(ott):
    ott_service = ['통합', '넷플릭스', '웨이브', '티빙', '디즈니+', '왓챠', '박스오피스']
    ranking_list = ranking_tuple[ott]
    return render_template('ranking.html', ranking_list = ranking_list, value = ott, ott_service = ott_service)
        

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__)) #현재 파일이 있는 디렉토리 절대 경로
    dbfile = os.path.join(basedir, 'db.sqlite') #데이터베이스 파일을 만든다

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다
    app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

    csrf = CSRFProtect()
    csrf.init_app(app)

#    db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장
    db.init_app(app) #app설정값 초기화
    db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
    db.create_all() #DB생성

    ranking_tuple = ranking() 

    app.run(host="127.0.0.1", port="8083", debug=True)