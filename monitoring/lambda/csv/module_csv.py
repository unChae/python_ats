# import modules
import boto3
import datetime
import pandas as pd

# init
client = boto3.client('s3')

def get_csv():
  bucket_name = 'ats-data-bucket'
  try:
    #current
    c_now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d-%H:%M:%S')
    c_date = c_now[0:10]
    c_hour = c_now[0:13]
    c_file_name = c_date + '/' + c_hour + '.csv'
    c_resp = client.get_object(Bucket=bucket_name, Key=c_file_name)
    c_df = pd.read_csv(c_resp['Body'], sep=',')
    
    #before
    b_now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d-%H:%M:%S')
    b_date = b_now[0:10]
    b_hour = b_now[0:13]
    b_file_name = b_date + '/' + b_hour + '.csv'
    b_resp = client.get_object(Bucket=bucket_name, Key=b_file_name)
    b_df = pd.read_csv(b_resp['Body'], sep=',')
    
    data = b_df.append(c_df)
    return data
        
  except Exception as err:
    print(err)