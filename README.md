#Approach:
Songs will be loaded into cloud search for easy search across all parameters. 
Till today (sep, 2017) there is no way to pause cloud search usage. Till AWS fixes this, approach is to load the data into dynamo.

#Steps:
1) Scrape the songs from wiki and store in local files. As is tamil songs between 1999 and 2018 is scraped. This can be movied in moviesList.py.

> python moviesList.py

2) Create a cloud search batch 

> python prepareCSBatch.py

3) Load the cloud search batch to dynamodb

> python loadToDynamoDB.py