import re 
from textblob import TextBlob  
import pandas as pd
import numpy as np
from Data_collection import tweet_collect
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import Stream

class TweetAnalyzer():
    """
    Preprocessing and analyaing the tweets with textblob.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text[:150] for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
 
        return df


"""
DOING SENTIMENT ANALYSIS WITH TEXTBLOB
"""

def predicting_Sentiment(tweets,query):
	df = tweet_analyzer.tweets_to_data_frame(tweets)
	print(len(df))
	df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
	positive=100*len(df['sentiment'][df['sentiment']==1])/len(df)
	negative=100*len(df['sentiment'][df['sentiment']==-1])/len(df)
	t_score=positive+negative
	score=(positive)/negative

	print('{} positive {}%'.format(query,100*len(df['sentiment'][df['sentiment']==1])/len(df)))
	print('{} negative {}%'.format(query,100*len(df['sentiment'][df['sentiment']==-1])/len(df)))
	print('{} neutral {}%'.format(query,00*len(df['sentiment'][df['sentiment']==0])/len(df)))

	file=str(query)+'.csv'
	df.to_csv(file)
	return score

"""
Calculating voting percentage among different parties.
"""

def voting_percentage(aap_score,bjp_score,cong_score):

	print('AAP Adjusted Voting Percentage  {}'.format(100*(aap_score )/((aap_score)+bjp_score+cong_score)))
	print('BJP Adjusted Voting Percentage  {}'.format(100*(bjp_score)/(aap_score+(bjp_score)+cong_score)))
	print('cong Adjusted Voting Percentage  {}'.format(100*(cong_score)/(aap_score+bjp_score+(cong_score))))

def main():

	with open('API_key.json') as json_file:
		data = json.load(json_file)
		for Key in API['Key']:
			API_Key=Key['API_KEY']
			API_SECRET=Key['API_SECRET']

	auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)

	api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
	

	parser=argparse.ArgumnetParser()

	parser.add_argument('query_keyword',help='Name of party which tweets you want to extract')
	parser.add_argument('MaxTweets',help='Number of Tweets you want to get')
	
	
	query= parser.query_keyword
	maxTweets=parser.MaxTweets
	
	tweets=[]
	
	"""
	Collecting Data on basis of Date i have collected data from 1 feb 20 to 8 feb 20 So there should be not any bias due to final results. 

	"""
	for i in range(1,9):
		until='2020-2-'+str(i)
		tweet_on=tweet_collect(query=query,maxTweets=maxTweets,until=until)
		tweets=tweets+tweet_on

	score=predicting_Sentiment(tweets,query)
	
	"""
	After getting scores for all three parties AAP,BJP and CONGRESS use
	voting_percentage function to get the ouput result.
	"""

if __name__ == '__main__':
	main()
	