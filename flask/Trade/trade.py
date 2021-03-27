from flask import request, url_for, redirect
from flask_restx import Resource, Api, Namespace, fields

import pymysql
from pymysql.cursors import DictCursor
from operator import itemgetter

import sys
sys.path.append("/root/ats")
from create_log import createLogs
#response
sys.path.append("/root/ats/flask")
from make_response import cus_respones

sys.path.append("/root/ats/flask/DB")
from connect_db import conn_db

sys.path.append("/root/ats/flask/UpbitApi")
from upbit_api import get_asset, sell_order, current_data

Trade = Namespace('Trade')

#자산내역 가져오기
@Trade.route('/get_trades')
class GetTrade(Resource):
  def post(self):
    
    conn = conn_db()
    cursor = conn.cursor()
          
    get_data = request.get_json()
    user_login_id = get_data['user_id']
    
    # trades_sql = '''
    #   select * 
    #   from Trades as t
    #   join Users as u
    #   on t.user_id = u.user_id
    #   join Settings as s
    #   on t.user_id = s.user_id
    #   where u.user_login_id = %s and t.trade_status != 0;
    # '''
    # value = (user_login_id)
    # cursor.execute(trades_sql, value)
    # trade_data = cursor.fetchall()
    payload = {"user_login_id": user_login_id}
    trade_data = get_trades(payload)
    
    #TRADEs 데이터에 코인 정보를 객체로 넣어준다
    count = 0
    for i in trade_data:
      # markets_sql = "select * from Markets where market_id = %s"
      # cursor.execute(markets_sql, i.get('market_id'))
      # market_data = cursor.fetchone()
      payload = {"market_id": i.get('market_id')}
      market_data = get_market(payload)
      trade_data[count]['market'] = market_data
      trade_data[count]['asset'] = get_market_profit(market_data['market_code'])
      count +=1
   
    if trade_data is None:
    #데이터가 없을경우
      createLogs(1, "No_data")
      return cus_respones(400, "no_data", "none")
    else:
    #데이터가 있을경우
      createLogs(1, "Get Trades")
      return cus_respones(200, "ok", trade_data)

#자산내역 가져오기
@Trade.route('/get_histories')
class GetTrade(Resource):
  def post(self):
    
    conn = conn_db()
    cursor = conn.cursor()
          
    get_data = request.get_json()
    user_login_id = get_data['user_id']
    
    trades_sql = '''
      select * 
      from Trades as t
      join Users as u
      on t.user_id = u.user_id
      join Settings as s
      on t.user_id = s.user_id
      where u.user_login_id = %s and t.trade_status != 1;
    '''
    value = (user_login_id)
    cursor.execute(trades_sql, value)
    trade_data = cursor.fetchall()
    
    #TRADEs 데이터에 코인 정보를 객체로 넣어준다
    count = 0
    for i in trade_data:
      markets_sql = "select * from Markets where market_id = %s"
      cursor.execute(markets_sql, i.get('market_id'))
      market_data = cursor.fetchone()
      trade_data[count]['market'] = market_data
      trade_data[count]['asset'] = get_market_profit(market_data['market_code'])
      count +=1
   
    if trade_data is None:
    #데이터가 없을경우
      createLogs(1, "No_data")
      return cus_respones(400, "no_data", "none")
    else:
    #데이터가 있을경우
      createLogs(1, "Get Trades")
      return cus_respones(200, "ok", trade_data)


#매도
@Trade.route('/sell_trade')
class SellTrade(Resource):
  def put(self):
    
    conn = conn_db()
    cursor = conn.cursor()
    
    get_data = request.get_json()
    user_id = get_data['user_id']
    market = get_data['market_code']
    
    # 마켓코드를 받아와서 매도 
    # a = sell_order(market)
    # return a.json()
    
    # trades_sql = '''
    #   UPDATE Trades AS t 
    #   JOIN Markets as m
    #   ON t.market_id = m.market_id
    #   JOIN Users AS u
    #   ON t.user_id = u.user_id
    #   SET t.trade_status = 0
    #   WHERE u.user_id = %s AND setting_id = %s AND m.market_code = %s 
    # '''
    # trades_value = (user_id, setting_id, market)
    # cursor.execute(trades_sql, trades_value)
    # conn.commit() 
    
    payload = {"user_id": user_id, "setting_id": setting_id, "market_code": market}
    update_trade_status(payload)
    
    
    # trades_sql = '''
    #   select * 
    #   from Trades as t
    #   join Users as u
    #   on t.user_id = u.user_id
    #   join Settings as s
    #   on t.user_id = s.user_id
    #   where u.user_login_id = %s and t.trade_status != 0;
    # '''
    # value = (user_login_id)
    # cursor.execute(trades_sql, value)
    # trade_data = cursor.fetchall()
    
    payload = {"user_id": user_id}
    trade_data = get_trades2(payload)
    
    #TRADEs 데이터에 코인 정보를 객체로 넣어준다
    count = 0
    for i in trade_data:
      # markets_sql = "select * from Markets where market_id = %s"
      # cursor.execute(markets_sql, i.get('market_id'))
      payload = {"market_code": i.get("market_id")}
      trade_data[count]['market'] = get_market(payload)
      trade_data[count]['asset'] = get_asset_data("KRW-KRW")
      trade_data[count]['market_profit'] = get_market_profit('market')
      count +=1
      
    if trade_data is None:
    #데이터가 없을경우
      conn.close()
      createLogs(1, "No_data")
      return cus_respones(400, "no_data", "none")
    else:
    #데이터가 있을경우
      conn.close()
      createLogs(1, "Get Setting")
      return cus_respones(200, "ok", trade_data)
      
   

# 코인 수익룰 키값 market_profit
# 전체 수익률 키값 avg_profit  trades_info 
# 평가금액 = 보유수량 * 현재가 소수점1번쨰에서 반올림해줘야한다
# 매입금액 = 보유수량 * 매입단가 소수점1번쨰에서 반올림해줘야한다
# 평가손익 = 평가금액 - 매입금액 - 수수료
# 수익률   = 평가손익 / 매입금액 * 100 소수점3번쨰에서 반올림해줘야한다
# 수수료 계산법
# 평가 금액 * % / 100   
def get_market_profit(market_code):
  
  asset =  get_asset(market_code)
  
  #보유수량
  volume = asset['balance']
  
  #현재가
  current_prices = current_data(market_code)
  
  #매입 단가
  avg_buy_price = asset['avg_buy_price']
  
  #평가 금액
  evaluation_price = float(volume) * float(current_prices)
  
  #매입 금액
  purchase_price = float(volume) * float(avg_buy_price)
  
  #평가손익
  evaluation_margin = round(evaluation_price) - round(purchase_price)
  
  #수익률
  profit = evaluation_margin / round(purchase_price) * 100
  
  #수수료
  # commission = evaluation_price * 0.05 /100
  #수익률 수수료 포함 버전
  # market_profit = evaluation_price / purchase_price * 100
  # asset['market_profit'] = str(round(profit, 2))+"%"
  asset['market_profit'] = round(profit, 2)
  return asset
  
  
  
  
  
  
  
    
 