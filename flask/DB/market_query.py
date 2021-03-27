import pymysql
from pymysql.cursors import DictCursor
import json
from connect_db import conn_db
import datetime
  
def get_marketCode():
    conn = conn_db()
    cursor = conn.cursor()
    
    query = "select market_code from Markets order by market_code;"
    cursor.execute(query)
    
    return cursor.fetchall()