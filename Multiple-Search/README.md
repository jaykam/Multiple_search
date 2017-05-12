# Multiple Search
Multiple Resource Search, REST API using Python

This repository contains source code of the API which parallely searches a query using multiprocessing module of python on Google, Twitter and DuckDuckGo and gives a simple result containing description from these three engines in JSON format.

Usage -   
https://quick-search.herokuapp.com/query
curl https://quick-search.herokuapp.com/query

change these keys to run the code in app.py

twitter_api_key = "twitter api key"
twitter_api_secret = "twitter api secret"
google_key = "google key"
google_secret = "google secret"
consumer_key = 'consumer key'
consumer_secret = 'consumer secret'
 