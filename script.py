
from twitter_keys import UserKeys
import os, oauth2, json, csv,time

def authenticate():
	user = UserKeys().user1()
	consumer = oauth2.Consumer(key=user["CONSUMER_KEY"], secret=user["CONSUMER_SECRET"])
	access_token = oauth2.Token(key=user["ACCESS_KEY"], secret=user["ACCESS_SECRET"])
	client = oauth2.Client(consumer, access_token)

	return client

def get_data(search,times):

	response,data = client.request(search,"GET")
	data =  json.loads(data)

	tweets = []

	for status in data["statuses"]:
		# package api call data into dict
		temp = {}
		temp["tweet"] = status["text"]
		temp["user_id"] = status["user"]["id"]
		temp["tweet_coordinates"] = status["coordinates"]
		temp["num_mentions"] = len(status["entities"]["user_mentions"])
		temp["retweeted"] = status["retweeted"]
		temp["num_followers"] = status["user"]["followers_count"]
		temp["num_friends"] = status["user"]["friends_count"]
		temp["user_description"] = status["user"]["description"]
		temp["member_since"] = status["user"]["created_at"]
		temp["tweet_created_at"] = status["created_at"]
		temp["time_zone"] = status["user"]["time_zone"]

		tweets.append(temp)

	return tweets


def sava_data(data,search_name):

	path = os.path.dirname(os.path.abspath('script.py'))
	# Create unique file name everytime script was run
	file_name = path+"/logs/"+search_name+time.strftime("_%m_%d_%Y_%H_%M_%S")+".csv"

	new_log = open(file_name,'a')
	log_writer = csv.writer(new_log)

	# title row
	title = ['user_id','tweet_created_at', 'member_since','tweet','retweeted','time_zone', 'num_followers','num_mentions', 'user_description','tweet_coordinates','num_friends']
	log_writer.writerow(title)

	# iterate through list of dicts and write a new line for each dict
	for item in data:

		temp = []

		for key,val in item.iteritems():
			if type(val) == unicode:
				val = val.encode('utf-8')
			temp.append(val)

		log_writer.writerow(temp)
    
	new_log.close()

if __name__ == "__main__":

	client = authenticate()
	data = get_data("https://api.twitter.com/1.1/search/tweets.json?q=%40trump&count=100",1)
	sava_data(data,"Donald_Trump")
	