import pymysql
from pymysql.cursors import DictCursor
import json
from connect_db import conn_db

# - Trades-

#get_trades
#자산내역 가져오기
def get_trades(payload):
  
  conn = conn_db()
  ursor = conn.cursor()

  query = '''
    select * 
    from Trades as t
    join Users as u
    on t.user_id = u.user_id
    join Settings as s
    on t.user_id = s.user_id
    where u.user_login_id = %s and t.trade_status != 0;
  '''
  _payload = (payload['user_login_id'])
  cursor.execute(query, _payload)
  
  return trade_data
  
#get_trades
#코인하나 정보 가져오기
def get_market(payload):
  
  conn = conn_db()
  ursor = conn.cursor()
  
  query = "select * from Markets where market_id = %s"
  cursor.execute(query, payload['market_id'])
  return cursor.fetchone()

#sell_trade
#판매상태 수정
def update_trade_status(payload):
  
  query = '''
    UPDATE Trades AS t 
    JOIN Markets as m
    ON t.market_id = m.market_id
    JOIN Users AS u
    ON t.user_id = u.user_id
    SET t.trade_status = 0
    WHERE u.user_id = %s AND setting_id = %s AND m.market_code = %s 
  '''
  _payload = (payload['user_id'], payload['setting_id, market'], payload["market_code"])
  cursor.execute(query, _payload)
  conn.commit()
  

def get_trades2(payload):
  
  conn = conn_db()
  ursor = conn.cursor()

  query = '''
    select * 
    from Trades as t
    join Users as u
    on t.user_id = u.user_id
    join Settings as s
    on t.user_id = s.user_id
    where u.user_id = %s and t.trade_status != 0;
  '''
  _payload = (payload['user_id'])
  cursor.execute(query, _payload)
  
  return trade_data