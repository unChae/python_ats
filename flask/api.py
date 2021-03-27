from flask import Flask  
from flask_restx import Resource , Api
from flask_cors import CORS
import pymysql
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
#하위폴더 import
from Users import auth
from Users import mypage
from Reservation import reservation
from Trade import trade
app = Flask(__name__)

CORS(app)
api = Api(
    app
)

api.add_namespace(auth.Auth, '/auth')
api.add_namespace(mypage.Mypage, '/mypage')
api.add_namespace(reservation.Reservation, '/reservation')
api.add_namespace(trade.Trade, '/trade')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)