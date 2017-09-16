import os
import boto3
import json
from pprint import pprint

movies = []
dMovies = {}

client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
response = client.list_tables()
print(response)


try:
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'movieTitle',
                'AttributeType': 'S',
            },
            {
                'AttributeName': 'Title',
                'AttributeType': 'S',
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'movieTitle',
                'KeyType': 'HASH',
            },
            {
                'AttributeName': 'Title',
                'KeyType': 'RANGE',
            },
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
    dynamoMovie = {}
    for key, value in movie["fields"].items():
        if(value and value.strip() <> ''):
            dynamoMovie[key.strip().replace('(', '').replace(')', '')] = {"S": value}
    songTitleMovieTitle = dynamoMovie["movieTitle"]["S"] + dynamoMovie["Title"]["S"]
    if(songTitleMovieTitle not in keys):
        keys.append(songTitleMovieTitle)
        dynamoMovies.append({"PutRequest": {"Item": dynamoMovie}})
    batchSize += 1
    if(batchSize == 24):
        movieList = {"MovieList": dynamoMovies}
        response = client.batch_write_item(RequestItems=movieList)
        with open('./batches/ddbBatch.json', 'a') as f:
            f.write(json.dumps(dynamoMovies))
        dynamoMovies = []
        batchSize = 0
