from flask import request, url_for, redirect
from flask_restx import Resource, Api, Namespace, fields
import json
import math

import pymysql
from pymysql.cursors import DictCursor

import sys
sys.path.append("/root/ats")
from create_log import createLogs
#response
sys.path.append("/root/ats/flask")
from make_response import cus_respones

sys.path.append("/root/ats/flask/DB")
from connect_db import conn_db
from user_query import *

sys.path.append("/root/ats/flask/UpbitApi")
from upbit_api import get_asset

Auth = Namespace('Auth')

#회원가입
@Auth.route('/register')
class Register(Resource):
    def post(self):
        
        conn = conn_db()
        cursor = conn.cursor()
        
        get_data = request.get_json()
        user_login_id = get_data['user_id']
        user_login_pw = get_data['user_password']
        user_name = get_data['user_name']
         
        # users_sql = "insert into Users(user_login_id, user_login_pw, user_name) values(%s, %s, %s);"
        # users_val = (user_login_id, user_login_pw, user_name)
        
        # cursor.execute(users_sql, users_val)
        # conn.commit() 
        # conn.close()
        payload = {'user_login_id': user_login_id, 'user_login_pw': user_login_pw, 'user_name':user_name}
        set_user(payload)
        
        
        return {
          "succes":"ok"
        }
      
#로그인
@Auth.route('/login')
class Login(Resource):
    def post(self):
        
        conn = conn_db()
        cursor = conn.cursor()
        
        get_data = request.get_json()
        user_login_id = get_data['user_id']
        user_login_pw = get_data['user_password']
    
        payload ={'user_login_id': user_login_id}
        user_pw = get_user_pw(payload)
        
        #비밀번호 체크
        if user_login_pw != user_pw.get('user_login_pw'):
            createLogs(2, "Incorrect password")
            return cus_respones(400, "Incorrect password", "none"), 409
        else:
            createLogs(2, "USER: "+ user_login_id +"login")
            return cus_respones(200, True , {"user_id": user_login_id})

#w전체 수익률 추가해야함
#전체 수익룰은 현재 거래되고 있는 코인들만 가져와서 계산하면됨 
#이익 = 평가금액 - 매입금액
#수익률 = 평가손익 / 매입금액 * 100 소수점3번쨰에서 반올림
@Auth.route('/token')
class Token(Resource):
    def post(self):
        
        conn = conn_db()
        cursor = conn.cursor()
        
        get_data = request.get_json()    
        user_login_id = get_data['user_id']
        
        
        #사용자 유무 확인
        if user_login_id == "":
            return cus_respones(400, "No Session", "none")
        else:
            payload = {"user_login_id": user_login_id}
            get_token(payload)
        
            response = get_token(payload)
            current_money = get_asset("KRW-KRW")["balance"]
            
            response["user_id"] = response.get('user_login_id')
            response["current_money"] = math.trunc(float(current_money))
            response["avg_profit"] = 40
            return cus_respones(200, "ok", response)
