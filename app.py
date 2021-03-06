import os
import json
import sys
import urllib
import tweepy
from flask import Flask, jsonify
from tweepy.parsers import JSONParser
from multiprocessing import Process, Queue
import pprint

app = Flask(__name__)

twitter_api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
twitter_api_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
google_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
google_secret = "xxxxxxxxxxxxxxxx"
consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(twitter_api_key, twitter_api_secret)
api = tweepy.API(auth,
			   wait_on_rate_limit=True,
			   wait_on_rate_limit_notify=True,
			   parser=tweepy.parsers.JSONParser()
			   )
if (not api):
	print ("Authentication Error")
	sys.exit (-1)


#Storing results
final_data = Queue()		


#DuckDuckGo instant API
def DuckduckGo(query):
	
	url = "https://api.duckduckgo.com/?q=%s&format=json&pretty=1" % query 
	duckduckgo_response = urllib.urlopen(url)
	data = json.loads(duckduckgo_response.read())

	final_data.put(data)
	


#Google Search API
def Google(query):
	google_result = {
		"google": {
			"url": "", 
			"text": ""
		}
	}
	google_url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s&fields=items/pagemap/website/description" % (google_key,google_secret,query)
	google_response = urllib.urlopen(google_url)
	data = json.loads(google_response.read())
	try:
		google_result = {
			"google": {
				"url": google_url,
				"text": data["items"][0]["pagemap"]["website"][0]["description"]
			}
		}
	except Exception:
		pass
	final_data.put(google_result)

#Twitter API
def Twitter(query):
	twitter_text=""
	twitter_result = {
		"twitter": {
			"url": "",
			"text": ""
		}
	}
	twitter_response = api.search(q=query, count=1)
	try:
		twitter_data = twitter_response["statuses"][0]["text"]
	except Exception:
		pass
	final_data.put(
		{
			"twitter": {
				"url": "", 
				"text": twitter_data
			}
		}	
	)


@app.route("/")
def index():
	return """
			<html>
			<body style='font-family="Helvetica, sans-serif"'>
			<h1>Multiple Search</h1>
			<h4>Multiple Resource Search REST API using Python</h4> <br>
			<h3>About</h3>
			<p>This API searches for a query on Google, Twitter and DuckDuckGo in parallel 
			using multiprocessing module of python and gives a combined result quickly which
			contains the description from these three engines in JSON format.
			</p>
			<br>
			<h3>Usage</h3>
			steps for run it on herokuapp : <br>
			<p>https://multiple-search.herokuapp.com/query <br> 
			curl https://quick-search.herokuapp.com/query</p>
			<br>
			<br>
			<h3><a href="https://github.com/jaykam/Multiple_search/">github link code</a></h3>
			<br>
			<br>

				<footer class="footer">
				<br>
					Contact : <br>
					Name : Jatin Kumar Mittal<br>
					Email : jatinmittal52@gmail.com<br>
					

				</footer>
			</body>
			</html>
			"""		


@app.route("/<query>")
def main(query):
	p1 = Process(target=Google, args=(query,))
	p1.start()
	p2 = Process(target=DuckduckGo, args=(query,))
	p2.start()
	p3 = Process(target=Twitter, args=(query,))
	p3.start()
	
	p1.join()
	p2.join()
	p3.join()

	result = {"query": query,
			"results": [
				final_data.get(),
				final_data.get(),
				final_data.get()
			]
		}
	
	return jsonify(result)


if __name__ == "__main__":
	app.run(debug=True)
