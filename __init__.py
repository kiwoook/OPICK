import os
import sched
from webbrowser import BackgroundBrowser #디렉토리 절대 경로
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler


from flask import session #세션
from flask_wtf.csrf import CSRFProtect #csrf
from models import db
from models import User
from form import RegisterForm, LoginForm
from rank_crawling import ranking
from movie import *

# 하루에 한번 크롤링 함수가 실행되게 하는 함수
def everyday_crawling():
    # 랭킹 튜플 전역변수화
    global ranking_tuple
    ranking_tuple = ranking()
sched = APScheduler()


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def mainpage():
    email = session.get('email', None)

    # 인기 작품 데이터 반환
    popular_list = TMDB_Trending()

    # 이메일 세션 처리 
    if(email != None):
        userinfo = User.query.filter_by(email=email).first()
        username = userinfo.username
        session['username'] = username
        return render_template('index.html',username=username,email=email, popular_list = popular_list)

    return render_template('index.html',email=email, popular_list = popular_list)
    
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

# TV 프로그램 상세 정보 페이지
@app.route('/tv/<int:id>')
def tv(id):
    tv_info, recommended_list = TV_Deatail(id)
    return render_template('tv_detailed_demo.html', tv_info = tv_info, list = recommended_list)

# 영화 상세 정보 페이지
@app.route('/movie/<int:id>')
def movie(id):
    mv_info, recommended_list = Movie_Deatail(id)
    return render_template('movie_detailed_demo.html', mv_info = mv_info, list = recommended_list)

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

#   db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장
    db.init_app(app) #app설정값 초기화
    db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
    db.create_all() #DB생성

    ranking_tuple = ranking()

    #12시간 간격으로 실행
    sched.add_job(id = 'crawling', func=everyday_crawling, trigger = "interval", hours = 12)
    sched.start()

    app.run(host="0.0.0.0", port="5000", debug=True)