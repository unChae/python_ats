import boto3
import datetime

def csv_s3_upload() :
  # S3 Client 생성
  s3 = boto3.client('s3')
  
  # 업로드할 파일
  now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d-%H:%M:%S')
  folder_date = now[0:10]
  file_date = now[0:13]
  csv_path = '/root/ats/monitoring/csvs/' + file_date + '.csv'
  file_name = folder_date + '/' + file_date + '.csv'
  print(file_name)
  
  # bucket name
  bucket_name = 'ats-data-bucket'
  
  # 첫본째 매개변수 : 로컬에서 올릴 파일이름 
  # 두번째 매개변수 : S3 버킷 이름 
  # 세번째 매개변수 : 버킷에 저장될 파일 이름. 
  s3.upload_file(csv_path, bucket_name, file_name)



