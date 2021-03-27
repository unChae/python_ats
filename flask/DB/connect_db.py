import pymysql
from pymysql.cursors import DictCursor

def conn_db():
  #db 연결
  conn = pymysql.connect(
          user='ats', 
          passwd='rmatkddnjs4321!', 
          host='atsdatabase.cx1qr2mihmj5.ap-northeast-2.rds.amazonaws.com', 
          db='ats', 
          charset='utf8',
          cursorclass=pymysql.cursors.DictCursor
  )
  # cursor = conn.cursor()
  return conn