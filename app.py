from flask import Flask, request, jsonify, url_for, redirect, flash, session
from flask import render_template
from flask_restful import Resource, Api
import psycopg2
from credentials import DB
from itsdangerous import Signer, BadSignature


app = Flask(__name__)
app.secret_key='mysecretkey'

secret_key = 'mysecretkey'
signer = Signer(secret_key)

def get_db_connection():
    conn = psycopg2.connect(
        host=DB['host'],
        database=DB['database'],
        user=DB['user'],
        password=DB['password'],
        port=DB['port']
    )
    return conn

@app.route('/logout')
def logout():
    # 세션에서 사용자 정보 삭제
    session.pop('user_email', None)
    session.pop('user_name', None)

    return redirect(url_for('index'))


@app.route('/', methods=['GET','POST'])
def index():
    error_message=None
    user_email=session.get('user_email')
    user_name=session.get('user_name')

    if request.method == "POST":
        # 로그인 정보가 제출되었을때
        if 'user_email' in request.form and 'user_passwd' in request.form:
            email=request.form['user_email']
            password=request.form['user_passwd']

            # postgres 연결
            conn=get_db_connection()  
            print('postgres 연결 완료')
            cursor=conn.cursor()

            query="SELECT name, email FROM member where email = %s AND password = %s;"
            cursor.execute(query, (email, password))
            print(f'email: {email}, password:{password}')
            # 조회된 사용자 정보 가져오기
            member=cursor.fetchone()
            print(f'조회 결과: {member}')

            cursor.close()
            conn.close()

            if member:
                session['user_email']=member[1] # 세션에 email 저장
                session['user_name']=member[0]  # 세션에 name 저장
                return redirect(url_for('index'))
            else:
                error_message = "이메일 또는 비밀번호가 잘못되었습니다."

    print('email:', user_email)
    print('error_msg:',error_message)
    return render_template('index.html', user_email=user_email, user_name=user_name, error_message=error_message)

    
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/verify', methods=['POST'])
def verify():
    signed_data = request.form.get('signed_data')
    
    try:
        # 서명된 데이터를 검증
        original_data = signer.unsign(signed_data)
        return f"서명이 유효합니다. 원본 데이터: {original_data.decode('utf-8')}"
    except BadSignature:
        return "서명이 유효하지 않습니다!"

@app.route('/signup', methods=['GET','POST'])
def sign_up():
    # 회원가입 양식 작성했을 때
    if request.method == "POST":
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        print(f"name: {name}, email: {email}, password: {password}")  # 폼 데이터 출력

        conn = get_db_connection() # postgres 연결
        print('postgres 연결 완료')
        cursor=conn.cursor()

        # 제출된 폼 데이터를 member 테이블에 저장하기
        query="INSERT INTO member (name, email, password) values (%s, %s, %s);"
        cursor.execute(query, (name, email, password))
        print('쿼리 실행 완료')

        conn.commit() 
        print('커밋 완료')
        cursor.close()
        print('커서 닫기 완료')
        conn.close()
        print('DB 연결 끊기 완료')

        flash('회원가입이 완료되었습니다!')
        return render_template('index.html', user_name=name)

    return render_template('signup.html')



if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)