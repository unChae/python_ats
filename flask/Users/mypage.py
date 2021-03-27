from flask import request, url_for, redirect
from flask_restx import Resource, Api, Namespace, fields

import boto3
from boto3.dynamodb.conditions import Key

from decimal import Decimal
import datetime
import pymysql
from pymysql.cursors import DictCursor
import json

import sys
sys.path.append("/root/ats")
from create_log import createLogs

sys.path.append("/root/ats/flask")
from make_response import cus_respones

sys.path.append("/root/ats/flask/DB")
from connect_db import conn_db

Mypage = Namespace('Mypage')

#키 입력
@Mypage.route('/set_key')
class SetKey(Resource):
    def post(self):
        
        conn = conn_db()
        cursor = conn.cursor()
        
        get_data = request.get_json()
        user_login_id = get_data['user_id']
        access_key = get_data['access_key']
        secret_key = get_data['secret_key']
        
        get_user_id = "select user_id from Users where user_login_id = %s"
        cursor.execute(get_user_id, user_login_id)
        user_id = cursor.fetchone().get('user_id')
        
        keys_sql = "insert into ApiKeys(access_key, secret_key, user_id) values(%s, %s, %s);"
        keys_val = (access_key, secret_key, user_id)
        
        cursor.execute(keys_sql, keys_val)

        conn.commit() 
        
        return cus_respones(200, "insert api keys", {"access_key": access_key, "secret_key": secret_key})

#키 수정
@Mypage.route('/update_key')
class UpdateKey(Resource):
    def put(self):
        
        conn = conn_db()
        cursor = conn.cursor()
        
        get_data = request.get_json()      
        user_login_id = get_data['user_id']
        access_key = get_data['access_key']
        secret_key = get_data['secret_key']
        
        keys_sql = '''
            UPDATE ApiKeys AS k join Users AS u 
            ON k.user_id = u.user_id
            SET k.access_key = %s,
            k.secret_key = %s
            WHERE u.user_login_id = %s; 
        '''
        keys_value = (access_key, secret_key, user_login_id)
        cursor.execute(keys_sql, keys_value)
        conn.commit() 

        keys_sql = '''
            select k.*
            from ApiKeys as k 
            join Users as u 
            on u.user_id = k.user_id
            where u.user_login_id = %s
        '''
        
        cursor.execute(keys_sql, user_login_id)
        return cus_respones(200, "Get Keys", cursor.fetchone())
  