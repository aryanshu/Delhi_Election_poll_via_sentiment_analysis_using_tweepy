import re 
import sys
import jsonpickle
import os
import numpy as np
import time
import json


def tweet_collect(query,maxTweets=1000,fName='tweets.txt',until=None):
  sinceId = None
  tweets=[]
  max_id =-1000000

  tweetCount = 0
  searchQuery = query  
  tweetsPerQry = 100 
  with open(fName, 'w') as f:
      while tweetCount < maxTweets:
          try:
              if (max_id <= 0):
                  if (not sinceId):
                      new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang="en",wait_on_rate_limit=True,
                                geocode='28.644800,77.216721,20km',until=until)
                  else:
                      new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                              since_id=sinceId,lang="en",wait_on_rate_limit=True,
                                geocode='28.644800,77.216721,20km',until=until)
              else:
                  if (not sinceId):
                      new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang="en",wait_on_rate_limit=True,
                                geocode='28.644800,77.216721,20km',until=until,
                                              max_id=str(max_id - 1))
                  else:
                      new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang="en",wait_on_rate_limit=True,
                                geocode='28.644800,77.216721,20km',until=until,
                                              max_id=str(max_id - 1),
                                              since_id=sinceId)
              if not new_tweets:
                  print("No more tweets found")
                  break
              for tweet in new_tweets:
                  f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                          '\n')
                  tweets.append(tweet)
              tweetCount += len(new_tweets)
              print("Downloaded {0} tweets".format(tweetCount))
              max_id = new_tweets[-1].id
          except tweepy.TweepError as e:
              # Just exit if any error
              print("some error : " + str(e))
              break

  print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
  return tweets

