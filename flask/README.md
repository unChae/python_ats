### ATS(Auto Trading System)-flask
 
  - Users
    - auth.py
      - /auth/login()
        - methode : post
        - parameter :
          - user_id(string)
          - user_password(string)
        - return :
          - status(int) -> 200, 409, 404, 500
          - msg(string) -> true, false
          - data(array) -> none
    
    - mypage.py
      - /mypage/get_mypage
        - methode : post
        - parameter :
          - user_id(string)
        - return :
          - status(int) -> 200, 409, 404, 500
          - msg(string) -> true, false
          - data(array) -> {"acessce_key" : "acessce_key", "secret_key" : "secret_key" }
      
      - /mypage/update_key
        - methode : post
        - parameter :
          - acessce_key(string)
          - secret_key(string)
          - user_id(string)
        - return :
          - status(int) -> 200, 409, 404, 500
          - msg(string) -> true, false
          - data(array) ->  {"acessce_key" : "acessce_key", "secret_key" : "secret_key" }
  - Reservation
    - reservation.py
      - /reservation/get_settings
        - methode : post
        - parameter :
          - user_id(string)
        - return :
          - status(int) -> 200, 409, 404, 500
          - msg(string) -> true, false
          - data(array) -> [{ 
                  "setting_name": "setting_name", 
                  "market" : "coin_name", 
                  "setting_persent" : "0", 
                  "setting_time": setting_time, 
                  "setting_benefit" : "0",      
                  "setting_loss" : "0", 
                  "setting_price" : "0"
          }]
      
      - /reservation/set_setting
        - methode : post
        - parameter :
          - user_id(string)
          - setting_name(string)
          - market(string)
          - setting_persent(int)
          - setting_benefit(int)
          - setting_loss(int)
          - setting_price(int)
        - return :
          - status(int) -> 200, 409, 404, 500
          - msg(string) -> true, false
          - data(array) -> none
      
      - /reservation/setting_update
        - methode : put
        - parameter :
          - user_id(string)
          - setting_name(string)
          - market(string)
          - setting_persent(int)
          - setting_benefit(int)
          - setting_loss(int)
          - setting_price(int)
          - setting_change_name(sting)
        - return :
          - status(int) -> 200, 409, 404, 500
          - msg(string) -> true, false
          - data(array) -> none
      
      - /resvation/setting_delete
        - methode : delete
        - parameter : 
          - user_id(string)
          - setting_name(string)
        -return :
          - status(int) -> 200, 409, 404, 500
          - msg(string) -> true, false
          - data(array) -> none
    
      /reservation/get_setting
        - methode : post
        - parameter :
          - user_id(string)
          - setting_name(string)
        - return :
          - status(int) -> 200, 409, 404, 500
          - msg(string) -> true, false
          - data(array) -> { 
                "setting_name": "setting_name", 
                "setting_market_id" : "coin_name", 
                "setting_percent" : 0, 
                "setting_time": setting_time, 
                "setting_benefit" : "0", 
                "setting_loss" : "0", 
                "setting_price" : "0", 
                "setting_created_at", "setting_active" 
          }
          
      /reservation//get_market
        - methode : get
        - parameter : none
        - return :
          - status(int) -> 200, 409, 404, 500
          - msg(string) -> true, false
          - data(array) -> [{ "market": "coin_name" }]
  - Trade
    - /trade/get_trade.py
    - methode : post
    - parameter : 
      - user_id(sting)
    - return : 
        - status(int) -> 200, 409, 404, 500
        - msg(string) -> true, false
        - data(array) -> { 
    
            trade_price": "",
            "trade_status": "0",
            "trade_created_at": "2021-03-16 02:08:56",
            "user_id": "",
            "market_id": "",
            "setting_id": "",
            "user_id": "",
            "market": {
                "market_id": "",
                "market_code": "",
                "market_kor_name": "",
                "market_eng_name": ""
            },
            "asset": {
                "currency": "",
                "balance": "",
                "locked": "",
                "avg_buy_price": "",
                "avg_buy_price_modified": true,
                "unit_currency": ""
            }
        }
    - /trade/sell_trade
        
  

  - Response
    - make_response.py
      - createLogs()
        - parameter : 
          - code(int)
          - msg(string)
  - 
  
오늘 오류난건 mySQL 실행만하면 한번밖에 안되고 
pymysql.err.InterfaceError: (0, '') 에라가 남
고치는 방법
일단 DML = insert, update, delete 할떄에는 

conn.commit()
conn.close()
를 꼭 해줘야한다
그리고 
db를 연결하는 코드는 함수화해서 
conn 만 리턴시키고 
사용하는 함수에서
불러다 써야한다
ex) conn = conn_db()
    cursor = conn.cursor()
    