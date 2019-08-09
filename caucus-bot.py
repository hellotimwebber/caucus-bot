import tweepy
import urllib
import json
import urllib.request
import time
from datetime import datetime

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#load tracker data
with urllib.request.urlopen("http://data.desmoinesregister.com/iowa-caucus/candidate-tracker/data/visits_all.json") as url:
	data = json.loads(url.read().decode())

#get today's date	
todayDate = datetime.today().strftime('%Y-%m-%d')	
tweetDate = datetime.today().strftime('%B %d')

#declare variables and arrays
visitors = []
visitors2 = []
stringLen = 0
newStatus = ' '
	
#search for visits on today's date	
for x in data['visits']:
	counter = 0
	date = x['start'][:10]
	if date == todayDate:
		# print(x)
		y = x['cid']
		for z in data['candidates']:
			if z['id'] == y:
				a = z['name']
				for p in visitors:
					if p == a:
						counter = counter+1
		if counter == 0:
			visitors.append(a)
			stringLen = stringLen + len(a) + 2
			
#check if two tweets are necessary
checkLen = stringLen			
while checkLen > 200:
	r = visitors[0]
	visitors.remove(r)
	visitors2.append(r)
	checkLen = checkLen - len(r) - 2
				
#print certain strings depending on number of visitors				
if len(visitors) == 0:
	newStatus = 'There are no scheduled candidate visits in Iowa today. See who\'s coming next: https://data.desmoinesregister.com/iowa-caucus/candidate-tracker/'
if stringLen > 200:
	newStatus = 'In Iowa today, ' + tweetDate + ': ' + ', '.join(visitors) + '... (cont.) https://data.desmoinesregister.com/iowa-caucus/candidate-tracker/'
	api.update_status(newStatus)
	time.sleep(5)
	newStatus = 'Also in Iowa today: ' + ', '.join(visitors2) + '. More: https://data.desmoinesregister.com/iowa-caucus/candidate-tracker/'
else:
	newStatus = 'In Iowa today, ' + tweetDate + ': ' + ', '.join(visitors) + '. More: https://data.desmoinesregister.com/iowa-caucus/candidate-tracker/'
api.update_status(newStatus)
		
