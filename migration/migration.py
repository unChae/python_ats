import pymysql 

conn = pymysql.connect(host='atsdatabase.cx1qr2mihmj5.ap-northeast-2.rds.amazonaws.com', user='ats', password='rmatkddnjs4321!', db='ats', charset='utf8') 
cursor = conn.cursor() 

sql = """
CREATE TABLE Users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_login_id VARCHAR(50) UNIQUE NOT NULL,
    user_login_pw VARCHAR(50) NOT NULL,
    user_name VARCHAR(50) NOT NULL
);

CREATE TABLE Settings (
 	setting_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 	setting_name VARCHAR(50) NOT NULL,
 	setting_percent VARCHAR(50) NOT NULL,
 	setting_time VARCHAR(50) NOT NULL,
 	setting_benefit VARCHAR(50) NOT NULL,
 	setting_loss VARCHAR(50) NOT NULL,
 	setting_price VARCHAR(50) NOT NULL,
 	setting_active VARCHAR(50) NOT NULL,
 	setting_created_at VARCHAR(50) NOT NULL,
 	setting_market_id TEXT NOT NULL,
	user_id INT NOT NULL, 
	FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE Markets (
	market_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	market_code VARCHAR(50) NOT NULL,
	market_kor_name VARCHAR(50) NOT NULL,
	market_eng_name VARCHAR(50) NOT NULL
);

CREATE TABLE Trades (
	trade_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 	trade_status VARCHAR(50) NOT NULL,
 	trade_created_at VARCHAR(50) NOT NULL,
 	trade_price VARCHAR(100) NOT NULL,
 	trade_volume VARCHAR(100) NOT NULL,
 	trade_side VARCHAR(50) NOT NULL,
 	setting_id INT NOT NULL,
 	setting_benefit VARCHAR(50) NOT NULL,
 	setting_loss VARCHAR(50) NOT NULL,
	user_id INT NOT NULL, 
	FOREIGN KEY (user_id) REFERENCES Users (user_id),     
 	market_id INT NOT NULL,
 	FOREIGN KEY (market_id) REFERENCES Markets (market_id)
);

CREATE TABLE ApiKeys (
 	access_key VARCHAR(50) NOT NULL,
 	secret_key VARCHAR(50) NOT NULL,
 	user_id INT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES Users (user_id)
);
"""

sql2 = "alter table Settings add setting_price varchar(50) not null; "

print(sql)

cursor.execute(sql2) 

conn.commit() 
conn.close() 


#sql create문

#Users
# CREATE TABLE Users (
# 	user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
# 	user_login_id VARCHAR(50) NOT NULL,
# 	user_login_pw VARCHAR(50) NOT NULL,
# 	user_name VARCHAR(50) NOT NULL,
# );

#Settings
# CREATE TABLE Settings (
#  	setting_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#  	setting_name VARCHAR(50) NOT NULL,
#  	setting_percent VARCHAR(50) NOT NULL,
#  	setting_time VARCHAR(50) NOT NULL,
#  	setting_benefit VARCHAR(50) NOT NULL,
#  	setting_loss VARCHAR(50) NOT NULL,
#  	setting_active VARCHAR(50) NOT NULL,
#  	setting_created_at VARCHAR(50) NOT NULL,
#  	setting_market_id TEXT NOT NULL,
# 	user_id INT NOT NULL, 
# 	FOREIGN KEY (user_id) REFERENCES Users (user_id)
# );


#Markets
# CREATE TABLE Markets (
# 	market_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
# 	market_code VARCHAR(50) NOT NULL,
# 	market_kor_name VARCHAR(50) NOT NULL,
# 	market_eng_name VARCHAR(50) NOT NULL
# );

#Trades
# CREATE TABLE Trades (
#  	trade_price VARCHAR(50) NOT NULL,
#  	trade_status VARCHAR(50) NOT NULL,
#  	trade_created_at VARCHAR(50) NOT NULL,
# 	user_id INT NOT NULL, 
# 	FOREIGN KEY (user_id) REFERENCES Users (user_id),     
#  	market_id INT NOT NULL,
#  	FOREIGN KEY (market_id) REFERENCES Markets (market_id),
# 	setting_id INT NOT NULL,
# 	FOREIGN KEY (setting_id) REFERENCES Settings (setting_id)     
# );

#ApiKeys
# CREATE TABLE ApiKeys (
#  	access_key VARCHAR(50) NOT NULL,
#  	secret_key VARCHAR(50) NOT NULL,
#  	user_id INT NOT NULL,
# 	FOREIGN KEY (user_id) REFERENCES Users (user_id)
# );