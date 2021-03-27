# modules
import os
import datetime
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# init
load_dotenv(verbose=True)

# connect database
conn = pymysql.connect(
  user=os.getenv('DATABASE_USER'), 
  passwd=os.getenv('DATABASE_PASSWORD'), 
  host=os.getenv('DATABASE_HOST'), 
  db=os.getenv('DATABASE_NAME'), 
  charset='utf8',
  cursorclass=pymysql.cursors.DictCursor
)
cursor = conn.cursor()

def get_setting():
  query = '''
    SELECT * 
    FROM Settings;
  '''
  cursor.execute(query)
  return cursor.fetchall()

def get_trade() : 
  query = '''
    SELECT * 
    FROM Trades;
  '''
  cursor.execute(query)
  return cursor.fetchall()
  
# market_code
def get_market_code(payload):
  query = '''
    SELECT * 
    FROM Markets
    WHERE market_code = %s;
  '''
  cursor.execute(query, payload['market_code'])
  return cursor.fetchone()
  
# market_id
def get_market_name(payload) :
  query = '''
    SELECT *
    FROM Markets
    WHERE market_id = %s
  '''
  cursor.execute(query, payload['market_id'])
  return cursor.fetchone()
  
# user_id
def get_apikey(payload):
  query = '''
    SELECT * 
    FROM ApiKeys
    WHERE user_id = %s;
  '''
  cursor.execute(query, payload['user_id'])
  return cursor.fetchone()

# user_id
def get_user_key(payload):
  query = '''
    SELECT * 
    FROM ApiKeys
    WHERE user_id = %s;
  '''
  cursor.execute(query, payload['user_id'])
  return cursor.fetchone()
  
# user_id, setting_id
def get_setting_benefit(payload) :
  query = '''
    SELECT *
    FROM Settings
    WHERE user_id = %s AND setting_id = %s
  '''
  _payload = (payload['user_id'], payload['setting_id'])
  cursor.execute(query, _payload)
  return cursor.fetchall()
  
# user_id, setting_id, market_id
def set_trade_status(payload) :
  query = '''
    UPDATE Trades
    SET trade_status = '0'
    WHERE user_id = %s AND setting_id = %s AND market_id = %s
  '''
  _payload = (payload['user_id'], payload['setting_id'], payload['market_id'])
  cursor.execute(query, _payload)
  conn.commit()

# user_id, market_id
def get_trade_exist(payload):
  date = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d')
  query = '''
    SELECT * 
    FROM Trades
    WHERE user_id = %s AND trade_created_at LIKE %s AND market_id = %s;
  '''
  _payload = (payload['user_id'], date + "%", payload['market_id'])
  cursor.execute(query, _payload)
  if len(cursor.fetchall()) < 1:
    return False
  else:
    return True
  
def set_trade(payload):
  now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
  query = '''
    INSERT INTO Trades(
      user_id, 
      market_id, 
      setting_id,
      setting_loss,
      setting_benefit,
      trade_bid_identifier,
      trade_status,
      trade_created_at
    ) 
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
  '''
  _payload = (payload['user_id'], payload['market_id'], payload['setting_id'], payload['setting_loss'], payload['setting_benefit'], payload['trade_bid_identifier'],'1', now)
  cursor.execute(query, _payload)
  conn.commit() 
