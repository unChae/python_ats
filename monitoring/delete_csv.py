import os
import datetime

def delete_csv(csv_path) :
  if os.path.isfile(csv_path) :
    os.remove(csv_path)
    
if __name__ == '__main__':
  now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d-%H:%M:%S')
  date = now[0:13]
  file_name = date + '.csv'
  csv_path = '/root/ats/monitoring/csvs/' + file_name
  delete_csv(csv_path)
  
