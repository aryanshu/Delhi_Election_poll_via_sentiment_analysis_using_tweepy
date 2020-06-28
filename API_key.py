import json
"""
Enter your Tweepy api confidential here and run it before using other files. 
"""
API = {}
API['Key']=[]

API['Key'].append({
	'API_KEY':'#',
	'API_SECRET':'#'

	})


with open('API_key.json', 'w') as outfile:
    json.dump(API, outfile)

