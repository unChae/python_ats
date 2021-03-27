import pymysql
from pymysql.cursors import DictCursor
import json
from connect_db import conn_db
import datetime
  
# -Settings-
#get_market
def get_markets():
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = "select * from Markets order by market_kor_name;"
  cursor.execute(query)
  
  return cursor.fetchall()

#해당유저의 셋팅의 각각 코인정보 가져오기
#get_market
def get_setting_market(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = '''
    select s.setting_market_id 
    from Settings as s
    join Users as u
    on s.user_id = u.user_id
    where u.user_login_id = %s;
  '''
  cursor.execute(query, payload['user_login_id'])
  return cursor.fetchall()

#해당유저의 예약 이름 가져오기  
def get_setting_name(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = "select setting_name from Settings where user_id = %s"
  cursor.execute(query, payload['user_id'])
  return cursor.fetchall()

#유저아이디 가져오기
def get_user_id(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
    
  query = "select user_id from Users where user_login_id = %s"
  cursor.execute(query, payload['user_login_id'])
  return cursor.fetchone().get('user_id')

#예약 만들기
def insert_setting(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  setting_sql = '''
    insert into Settings(
    setting_name, 
    setting_percent, 
    setting_time,
    setting_benefit,
    setting_loss,
    setting_price,
    setting_active,
    setting_created_at,
    setting_market_id,
    user_id
    ) 
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
  '''
  #배열로 받은것을 문자열로 만들어서 넣어준다
  now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
  _payload = (payload['setting_name'], payload['setting_percent'], payload['setting_time'], payload['setting_benefit'], payload['setting_loss'], payload['setting_price'], "true", now, payload['setting_market_code'], payload['user_id'])
  cursor.execute(setting_sql, _payload)
  conn.commit()
  conn.close()

#예약 전부 조회
def get_settings(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = '''
    select s.* 
    from Settings as s
    join Users as u
    on s.user_id = u.user_id
    where u.user_login_id = %s;
  '''
    
  cursor.execute(query, payload['user_login_id'])
  return cursor.fetchall()
 
#해당 유저의 예약만 조회
def get_setting(payload):
     
  conn = conn_db()
  cursor = conn.cursor()
   
  query = '''
    select s.* 
    from Settings as s
    join Users as u
    on s.user_id = u.user_id
    where u.user_login_id = %s and s.setting_name = %s;
  '''
  _payload = (payload['user_login_id'], payload['setting_name'])
  cursor.execute(query, _payload)

  return cursor.fetchone()

#get_setting
#코인하나만 가져오기
def get_market(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = "select * from Markets where market_code = %s"
  cursor.execute(query, payload['market_code'])
  return cursor.fetchone()
  
#예약 수정
def update_setting(payload):
  
  conn = conn_db()
  cursor = conn.cursor()  
  
  query = '''
    UPDATE Settings AS s join Users AS u 
    ON s.user_id = u.user_id
    SET s.setting_name = %s, 
    s.setting_percent = %s,
    s.setting_time = %s,
    s.setting_benefit = %s,
    s.setting_loss = %s,
    s.setting_price = %s,
    s.setting_market_id = %s
    WHERE u.user_login_id = %s AND s.setting_id = %s; 
  '''
  _payload = (payload['setting_name'], payload['setting_percent'], payload['setting_time'], payload['setting_benefit'], payload['setting_loss'], payload['setting_price'],payload['setting_market_code'], payload['user_login_id'], payload['setting_id'])
  cursor.execute(query, _payload)
  conn.commit()
  conn.close()

#예약 삭제
def delete_setting(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = '''
    delete s from Settings as s 
    join Users as u 
    on s.user_id = u.user_id 
    where u.user_login_id = %s and s.setting_name = %s;
  '''
  _payload = (payload['user_login_id'], payload['setting_name'])
  cursor.execute(query, _payload)
  conn.commit()
  conn.close()
  
#셋팅 활성화 조회
def get_setting_active(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = '''
    select s.setting_active
    from Settings as s
    join Users as u
    on s.user_id = u.user_id
    where u.user_login_id = %s and s.setting_name = %s;
  '''
  _payload = (payload["user_login_id"], payload["setting_name"])
  cursor.execute(query, _payload)
  return cursor.fetchone().get('setting_active')

#셋팅 활성화 변경  
def update_setting_active(payload):
  
  conn = conn_db()
  cursor = conn.cursor()
  
  query = '''
    UPDATE Settings AS s join Users AS u 
    ON s.user_id = u.user_id
    SET s.setting_active = %s
    WHERE u.user_login_id = %s AND s.setting_name = %s; 
  '''
  _payload = (payload["active_status"], payload["user_login_id"], payload["setting_name"])
  cursor.execute(query, _payload)
  conn.commit()
  conn.close()