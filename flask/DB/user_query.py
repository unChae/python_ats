import pymysql
from pymysql.cursors import DictCursor
import json
from connect_db import conn_db

# - Users -
#회원가입
def set_user(payload):
  conn = conn_db()
  cursor = conn.cursor()
  
  query = "insert into Users(user_login_id, user_login_pw, user_name) values(%s, %s, %s);"
  _payload = (payload['user_login_id'], payload['user_login_pw'], payload['user_name'])
  
  cursor.execute(query, _payload)
  conn.commit() 
  conn.close()


#로그인
def get_user_pw(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = "select user_login_pw from Users where user_login_id = %s"
  _payload = (payload['user_login_id'])
        
  cursor.execute(query, _payload)
  response = cursor.fetchone()
  conn.close
  return response

#토큰
def get_token(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = '''
    select u.user_login_id, u.user_name, k.access_key, k.secret_key 
    from Users as u 
    join ApiKeys as k 
    on u.user_id = k.user_id
    where u.user_login_id = %s
  '''
  cursor.execute(query, payload['user_login_id'])
  response = cursor.fetchone()
  conn.close()
  return response
