import os
import boto3
import json
from pprint import pprint
import uuid

movies = []
dMovies = {}

client = boto3.client(
    'dynamodb', 
    endpoint_url='https://dynamodb.' + os.environ['AWS_DEFAULT_REGION'] + '.amazonaws.com',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
)
response = client.list_tables()

# if('MovieList' in response['TableNames']):
#     client.delete_table(TableName='MovieList)
#     print('Deleted MovieList table!')

try:
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'MovieTitle',
                'AttributeType': 'S',
            },
            {
                'AttributeName': 'Title',
                'AttributeType': 'S',
            },
            {
                'AttributeName': 'UniqueId',
                'AttributeType': 'S',
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'MovieTitle',
                'KeyType': 'HASH',
            },
            {
                'AttributeName': 'Title',
                'KeyType': 'RANGE',
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'uniqueSongs',
                'KeySchema': [
                    { 'AttributeName': "UniqueId", 'KeyType': "HASH"}
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        },
        TableName='MovieList',
    )
except client.exceptions.ResourceInUseException:
    print "Table already exists!"
    pass

with open('./batches/csBatch.json', 'r') as data_file:    
   movies = json.load(data_file)

movie = movies[0]
dynamoMovies = []
batchSize = 0

keys = []

for movie in movies:
    # dynamoMovie = {'Id': str(uuid.uuid4())}
    dynamoMovie = {}
    for key, value in movie["fields"].items():
        if(value and value.strip() <> ''):
            dynamoMovie[key.strip().replace('(', '').replace(')', '')] = {"S": value.strip().lower()}
    songTitleMovieTitle = dynamoMovie["MovieTitle"]["S"] + dynamoMovie["Title"]["S"]
    if(songTitleMovieTitle not in keys):
        keys.append(songTitleMovieTitle)
        dynamoMovies.append({"PutRequest": {"Item": dynamoMovie}})
    batchSize += 1
    if(batchSize == 24):
        movieList = {"MovieList": dynamoMovies}
        print(movieList)
        response = client.batch_write_item(RequestItems=movieList)
        with open('./batches/ddbBatch.json', 'a') as f:
            f.write(json.dumps(dynamoMovies))
        dynamoMovies = []
        batchSize = 0
