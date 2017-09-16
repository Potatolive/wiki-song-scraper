Batch program to scrape movie songs from wiki and load it to either dynamodb or cloud search.

# Approach:
1. Songs will be loaded into cloud search for easy search across all parameters. 
2. Till today (sep, 2017) there is no way to pause cloud search usage. 
3. Till AWS fixes this, approach is to load the data into dynamo. (https://forums.aws.amazon.com/thread.jspa?messageID=711615)

# Steps:
1) Scrape the songs from wiki and store in local files. Hard coded to scrape tamil songs between 1999 and 2018. This can be modified in moviesList.py.

> python moviesList.py

2) Create a cloud search batch 

> python prepareCSBatch.py

3) Load the cloud search batch to dynamodb

> python loadToDynamoDB.py

If you intend to load the data into cloudsearch instead of dynamodb, use aws console or cli to push "batches/csBatch.json" to your cloudsearch index.

# Configutation:
All aws configuration is handled using environment variables. Environment variables used

1. AWS_DEFAULT_REGION
2. AWS_ACCESS_KEY_ID
3. AWS_SECRET_ACCESS_KEY

# Caution
Have put togather a quick scraper and moving on to other tasks. No proper error handling!