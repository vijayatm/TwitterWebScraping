import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import tweepy
import codecs
from openpyxl import Workbook
import datetime
import unicodecsv as csv
import os

#Twitter API
consumer_key = "veJT9JSG1GkcipHea1FE46jfo"
consumer_secret = "u7vsqY3kLr3gFBbiveHolG4T8cA9Gg75vjk7iUyxvKcgByKslO"
access_key = "1647057175-RpRA4V1gFpzOpMC0P4TOVZTiAPddRHaRni9Z3G1"
access_secret = "2AZqJ64bOw8iAtswROdmnNjAfPFnkLZ31VzGzAihHfthm"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		# print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	print ('There are {alltweets} tweets in total' .format(alltweets=len(alltweets)))

	outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]

	with open('%s_tweets_1.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		print ('Writing the information in excel file')
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
		print ('Success! Your file is saved')
	pass

	
if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("ikamalhaasan")


