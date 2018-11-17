import tweepy #Tweepy pour jouer avec l'API Twitter
import time #Time pour avoir la date


consumer_key = 'XXXXXXXX'
consumer_secret = 'XXXXXXXX'
access_token = 'XXXXXXXX'
access_token_secret = 'XXXXXXXX'
####
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
### FIN DE CONNEXION A L'API TWITTER ###

### VERIFICATION DE CONNEXION ###
user = api.me() 
print (user.name) # Affiche mon nom




### FIN DE VERIFICATION DE CONNEXION ###
tauxRetweetAttendu = 90 # 50 / 90 / 90 / 90 / 90
tauxRetweetRTAttendu = 50 # 35 / 35 / 50 / 70 90
tauxRetweetFollowAttendu = 50 # 35 / 35 / 50 / 70 90

### VERIFICATION DE MES 200 DERNIERS TWEETS ###
retweetCount = 0
originalTweetCount = 0
retweetRTCount = 0
retweetFollowCount = 0
### FIN DE VERIFICATION DE MES 200 DERNIERS TWEETS ###

### VERIFICATION DE MES 200 DERNIERS TWEETS ###
statuses = api.user_timeline(id = user.id, count = 200)

for status in statuses:
	monText = status.text

	if monText.startswith("RT @") == True:
		print("Retweet !")
		retweetCount +=1
		rtPerRT = monText.count('RT')
		if rtPerRT > 1:
			print("RT trouvé")
			retweetRTCount +=1
		else:
			print("RT non présent")

		if "follow" in monText:
			print("Follow trouvé : ")	
			retweetFollowCount +=1
		else:
			print("Follow non présent")

	else:
		print("pas un Retweet !")
		originalTweetCount +=1
		print (monText)
print("Nbre total de retweet : "+ str(retweetCount))
print("Nbre total de Tweet : "+ str(originalTweetCount))
print("Nbre retweet avec RT : "+ str(retweetRTCount))
print("Nbre retweet avec Follow : "+ str(retweetFollowCount))
retweettaux = retweetCount * 100 / 200
retweetRTtaux = retweetRTCount * 100 / 200
retweetFollowtaux = retweetFollowCount * 100 / 200



if retweettaux > tauxRetweetAttendu:
	print ("FAIL - Nbre de retweet trop élevé : "+str(retweettaux)+"% au lieu de "+str(tauxRetweetAttendu)+"%")
	solutiontaux = retweetCount - (retweetCount * tauxRetweetAttendu / retweettaux)
	print("il manque "+str(solutiontaux)+" tweets")
else:
	print ("OK - Nbre de retweet : "+str(retweettaux)+"% au lieu de "+str(tauxRetweetAttendu)+"%")

if retweetRTtaux > tauxRetweetRTAttendu:
	print ("FAIL - Nbre de retweet avec RT trop élevé : "+str(retweetRTtaux)+"% au lieu de "+str(tauxRetweetRTAttendu)+"%")
	solutionRTtaux = retweetRTCount - (retweetRTCount * tauxRetweetRTAttendu / retweetRTtaux)
	print("il manque "+str(solutionRTtaux)+" retweets sans RT ou Follow")
else:
	print ("OK - Nbre de retweet : "+str(retweetRTtaux)+"% au lieu de "+str(tauxRetweetRTAttendu)+"%")

if retweetFollowtaux > tauxRetweetFollowAttendu:
	print ("FAIL - Nbre de retweet avec Follow trop élevé : "+str(retweetFollowtaux)+"% au lieu de "+str(tauxRetweetFollowAttendu)+"%")
else:
	print ("OK - Nbre de retweet : "+str(retweetFollowtaux)+"% au lieu de "+str(tauxRetweetFollowAttendu)+"%")



		### FIN DE VERIFICATION DE MES 200 DERNIERS TWEETS ###



