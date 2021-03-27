import boto3

def create_market_table(dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        
  table = dynamodb.create_table(
    TableName='Markets',
    KeySchema=[
      {
        'AttributeName': 'market',
        'KeyType': 'HASH'  # Partition key
      },
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'market',
        'AttributeType': 'S'
      },
    ],
    ProvisionedThroughput={
      'ReadCapacityUnits': 10,
      'WriteCapacityUnits': 10
    }
  )
  return table
    
def create_user_table(dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    
  table = dynamodb.create_table(
    TableName='Users',
    KeySchema=[
      {
        'AttributeName': 'user_id',
        'KeyType': 'HASH'  # Partition key
      },
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'user_id',
        'AttributeType': 'S'
      },
    ],
    ProvisionedThroughput={
      'ReadCapacityUnits': 10,
      'WriteCapacityUnits': 10
    }
  )
  return table
  
def create_key_table(dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    
  table = dynamodb.create_table(
    TableName='Keys',
    KeySchema=[
      {
        'AttributeName': 'user_id',
        'KeyType': 'HASH'  # Partition key
      },
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'user_id',
        'AttributeType': 'S'
      },
    ],
    ProvisionedThroughput={
      'ReadCapacityUnits': 10,
      'WriteCapacityUnits': 10
    }
  )
  return table
  
def create_setting_table(dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    
  table = dynamodb.create_table(
    TableName='Settings',
    KeySchema=[
      {
        'AttributeName': 'user_id',
        'KeyType': 'HASH'  # Partition key
      },
      {
        'AttributeName': 'setting_name',
        'KeyType': 'RANGE'  # Sort key
      },
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'user_id',
        'AttributeType': 'S'
      },
      {
        'AttributeName': 'setting_name',
        'AttributeType': 'S'
      },
    ],
    ProvisionedThroughput={
      'ReadCapacityUnits': 10,
      'WriteCapacityUnits': 10
    }
  )
  return table

def create_trade_table(dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    
  table = dynamodb.create_table(
    TableName='Trades',
    KeySchema=[
      {
        'AttributeName': 'user_id',
        'KeyType': 'HASH'  # Partition key
      },
      {
        'AttributeName': 'market',
        'KeyType': 'RANGE'
      },
    ],
    AttributeDefinitions=[
      {
        'AttributeName': 'user_id',
        'AttributeType': 'S'
      },
      {
        'AttributeName': 'market',
        'AttributeType': 'S'
      },
    ],
    ProvisionedThroughput={
      'ReadCapacityUnits': 10,
      'WriteCapacityUnits': 10
    }
  )
  return table
  
if __name__ == '__main__':
  try:
    market_table = create_market_table()
    print("Table status:", market_table.table_status)
  except:
    print('already exists: Markets')
        
  try:
    user_table = create_user_table()
    print("Table status:", user_table.table_status)
  except:
    print('already exists: Users')
    
  try:
    key_table = create_key_table()
    print("Table status:", key_table.table_status)
  except:
    print('already exists: Keys')
    
  try:
    setting_table = create_setting_table()
    print("Table status:", setting_table.table_status)
  except:
    print('already exists: Settings')
    
  try:
    trade_table = create_trade_table()
    print("Table status:", trade_table.table_status)
  except ValueError:
    print(ValueError)
