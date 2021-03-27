#benefit 얼마익절 #price 자산의 얼마를 넣을것이냐
from flask import request, url_for, redirect
from flask_restx import Resource, Api, Namespace, fields
import flask
import numpy as np
from decimal import Decimal
import datetime
import json
from operator import itemgetter

import pymysql
from pymysql.cursors import DictCursor

import sys
sys.path.append("/root/ats")
from create_log import createLogs

sys.path.append("/root/ats/flask")
from make_response import cus_respones

sys.path.append("/root/ats/flask/DB")
from connect_db import conn_db
from setting_query import *

Reservation = Namespace('Reservation')

#코인종류 넘겨주기
@Reservation.route('/get_market')
class GetMarket(Resource):
    def post(self):
      
      conn = conn_db()
      cursor = conn.cursor()
      
      get_data = request.get_json()
      user_login_id = get_data['user_id']
      
      # get_market = "select * from Markets order by market_kor_name;"
      # cursor.execute(get_market)
      
      # market_data = cursor.fetchall()
      
      
      # get_setting = '''
      #   select s.setting_market_id 
      #   from Settings as s
      #   join Users as u
      #   on s.user_id = u.user_id
      #   where u.user_login_id = %s;
      # '''
      
      # cursor.execute(get_setting, user_login_id)
      
      # settings_data = cursor.fetchall()
      
      market_data = get_markets()
      payload = {"user_login_id":user_login_id}
      settings_market_data = get_setting_market(payload)
      
      #setting에 있는 marketCode를 가져와서 한개의 배열로 만들어준다
      setting_market = []
      for i in settings_market_data:
        setting_market.extend(i.get('setting_market_id').split(','))
      
      #사용자가 이미 선택한 코인을 표시해준다
      response = []
      
      for i in market_data:
        response.append(i)
        response[-1]["active"]=False
        for j in setting_market:
          if i.get('market_code') == j:
            response[-1]["active"]=True
      
      return cus_respones(200, "marketData", response)
      

#셋팅하기
@Reservation.route('/set_setting')
class SetSetting(Resource):
    def post(self):
      
      conn = conn_db()
      cursor = conn.cursor()
   
      get_data = request.get_json()
      user_login_id = get_data['user_id']
      setting_name = get_data['setting_name']
      market_code = get_data['market']
      setting_percent = get_data['setting_percent']
      setting_time = get_data['setting_time']
      setting_benefit = get_data['setting_benefit']
      setting_loss = get_data['setting_loss']
      setting_price = get_data['setting_price']
      
      #user_id구하기
      # get_user_id = "select user_id from Users where user_login_id = %s"
      # cursor.execute(get_user_id, user_login_id)
      # user_id = cursor.fetchone().get('user_id')
      
      # get_setting_name = "select setting_name from Settings where user_id = %s"
      # cursor.execute(get_setting_name, user_id)
      
      # setting_sql = '''
      #   insert into Settings(
      #   setting_name, 
      #   setting_percent, 
      #   setting_time,
      #   setting_benefit,
      #   setting_loss,
      #   setting_price,
      #   setting_active,
      #   setting_created_at,
      #   setting_market_id,
      #   user_id
      #   ) 
      #   values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
      # '''
      # #배열로 받은것을 문자열로 만들어서 넣어준다
      
      # now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
      # settings_val = (setting_name, setting_percent, setting_time, setting_benefit, setting_loss, setting_price, "true", now, market_str, user_id)
      # cursor.execute(setting_sql, settings_val)
      # conn.commit()
      # conn.close()
      
      payload = {"user_login_id": user_login_id}
      user_id = get_user_id(payload)
      payload = {"user_id": user_id}
      _setting_name = get_setting_name(payload)
      #setting_name 구하기
      
      #중복된 예약이름이 있는지 검사
      for item in _setting_name:
        if setting_name == item.get('setting_name'):
          return cus_respones(400, "DuplicateName", "none"),409
      
      market_code = ",".join(market_code)
      payload = { 
        "setting_name": setting_name, 
        "setting_percent":setting_percent, 
        "setting_time":setting_time, 
        "setting_benefit":setting_benefit, 
        "setting_loss":setting_loss, 
        "setting_price":setting_price, 
        "setting_market_code":market_code, 
        "user_id": user_id 
      }    
      
      insert_setting(payload)
      createLogs(1, "Create setting")
      return cus_respones(200, "create reservation", "none")

#셋팅가져오기    
@Reservation.route('/get_settings')
class GetSettings(Resource):
    def post(self):
      
      conn = conn_db()
      cursor = conn.cursor()
      
      get_data = request.get_json()
      user_login_id = get_data['user_id']
      
      # settings_sql = '''
      #   select s.* 
      #   from Settings as s
      #   join Users as u
      #   on s.user_id = u.user_id
      #   where u.user_login_id = %s;
      # '''
      # cursor.execute(settings_sql, user_login_id)
      # response =  cursor.fetchall()
      
      payload = {"user_login_id": user_login_id}
      setting_data = get_settings(payload)
      
      #데이터 유무 검사
      if setting_data is None:
        createLogs(1, "No_data")
        return cus_respones(400, "no_data", "none")
      else:
        createLogs(1, "Get Setting")
        return cus_respones(200, "ok", setting_data)


#셋팅 하나만 가져오기    
@Reservation.route('/get_setting')
class GetSetting(Resource):
    def post(self):
      
      conn = conn_db()
      cursor = conn.cursor()
      
      get_data = request.get_json()
      user_login_id = get_data['user_id']
      setting_name = get_data['setting_name']
  
      # settings_sql = '''
      #       select s.* 
      #       from Settings as s
      #       join Users as u
      #       on s.user_id = u.user_id
      #       where u.user_login_id = %s and s.setting_name = %s;
      # '''
      # settings_value = (user_login_id, setting_name)
      # cursor.execute(settings_sql, settings_value)
      
      # #설정 코인을 배열로 변경해준다
      # setting_data = cursor.fetchone()
      # setting_market = setting_data.get('setting_market_id').split(',')
      
      payload = {"user_login_id": user_login_id, "setting_name": setting_name}
      setting_data = get_setting(payload)
      setting_market = setting_data.get('setting_market_id').split(',')
      
      
      #Settings 데이터에 코인 정보를 객체로 넣어준다
      market_data = []
      for item in setting_market:
        # markets_sql = "select * from Markets where market_code = %s"
        # cursor.execute(markets_sql, i)
        # market_data.append(cursor.fetchone())
        payload = {"market_code": item}
        market_data.append(get_market(payload))
      
      setting_data['setting_market_id'] = market_data
      
      if setting_data is None:
        createLogs(1, "No_data")
        return cus_respones(400, "no_data", "none")
      else:
        createLogs(1, "Get Setting")
        return cus_respones(200, "ok", setting_data)


#셋팅수정하기  
@Reservation.route('/update_setting')
class UpdateSetting(Resource):
    def put(self):
      
      conn = conn_db()
      cursor = conn.cursor()
      
      get_data = request.get_json()
      user_login_id = get_data['user_id']
      setting_id = get_data['setting_id']
      setting_name = get_data['setting_name']
      market = get_data['market']
      setting_percent = get_data['setting_percent']
      setting_time = get_data['setting_time']
      setting_benefit = get_data['setting_benefit']
      setting_loss = get_data['setting_loss']
      setting_price = get_data['setting_price']

      # settings_sql = '''
      #   UPDATE Settings AS s join Users AS u 
      #   ON s.user_id = u.user_id
      #   SET s.setting_name = %s, 
      #   s.setting_percent = %s,
      #   s.setting_time = %s,
      #   s.setting_benefit = %s,
      #   s.setting_loss = %s,
      #   s.setting_price = %s,
      #   s.setting_market_id = %s
      #   WHERE u.user_login_id = %s AND s.setting_id = %s; 
      # '''
      # market_code = ",".join(market)
      # settings_value = (setting_name, setting_percent, setting_time, setting_benefit, setting_loss, setting_price, market_str, user_login_id, setting_id)
      # cursor.execute(settings_sql, settings_value)
      # conn.commit()
      # conn.close()
      #마켓을 str로 바꿔준다
      market_code = ",".join(market)
      payload = { 
        "setting_name": setting_name, 
        "setting_percent":setting_percent, 
        "setting_time":setting_time, 
        "setting_benefit":setting_benefit, 
        "setting_loss":setting_loss, 
        "setting_price":setting_price, 
        "setting_market_code":market_code, 
        "user_login_id": user_login_id,
        "setting_id": setting_id
      }  
      update_setting(payload)
      
      createLogs(1, "Updata Setting")
      return cus_respones(200, "update Settings", "none")
  
@Reservation.route('/delete_setting')
class DeleteSetting(Resource):
    def post(self):
      
      conn = conn_db()
      cursor = conn.cursor()
      
      get_data = request.get_json()
      user_login_id = get_data['user_id']
      setting_name = get_data['setting_name']
      
      # settings_sql = '''
      #   delete s from Settings as s 
      #   join Users as u 
      #   on s.user_id = u.user_id 
      #   where u.user_login_id = %s and s.setting_name = %s;
      # '''
      # settings_value = (user_login_id, setting_name)
      # cursor.execute(settings_sql, settings_value)
      # conn.commit()
      # conn.close()
      payload = {"user_login_id": user_login_id, "setting_name": setting_name}
      delete_setting(payload)
      
      createLogs(1, "Delete Setting")
      return cus_respones(200, "ok", "none")

#예약 실행 여부 설정
@Reservation.route('/active_setting')
class ActiveSetting(Resource):
  def put(self):
    
    conn = conn_db()
    cursor = conn.cursor()
    
    get_data = request.get_json()
    user_login_id = get_data['user_id']
    setting_name = get_data['setting_name']
    
    #setting_active 조회
    # settings_sql = '''
    #   select s.setting_active
    #   from Settings as s
    #   join Users as u
    #   on s.user_id = u.user_id
    #   where u.user_login_id = %s and s.setting_name = %s;
    # '''
    # settings_value = (user_login_id, setting_name)
    # cursor.execute(settings_sql, settings_value)
    
    # active_status =  cursor.fetchone().get('setting_active')
    payload = {"user_login_id":user_login_id, "setting_name": setting_name}
    active_status = get_setting_active(payload)
    
    if active_status == "true":
      active_status = "false"
    elif active_status == "false":
      active_status = "true"
    
    #setting_active 수정
    # settings_sql = '''
    #   UPDATE Settings AS s join Users AS u 
    #   ON s.user_id = u.user_id
    #   SET s.setting_active = %s
    #   WHERE u.user_login_id = %s AND s.setting_name = %s; 
    # '''
    # settings_value = (active_status, user_login_id, setting_name)
    # cursor.execute(settings_sql, settings_value)
    # conn.commit()
    # conn.close()
    payload= {"setting_active": active_status, "user_login_id": user_login_id, "setting_name": setting_name}
    update_setting_active(payload)
    
    createLogs(1, "Active is "+active_status)
    return cus_respones(200, "true", {"setting_active": active_status})  
    
      
      