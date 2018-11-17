import tweepy #Tweepy pour jouer avec l'API Twitter
import time #Time pour avoir la date
import csv #CSV pour l'écriture dans un fichier
import re #re pour trouver les mentions
import random #pour avoir la ligne aléatoire pour les nouveaux tweets

### CONNEXION A L'API TWITTER ###
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
tweetNeeded = 20
tmpRechargeTweet = 600




def EnvoieUnTweet():
	newTweet = 0
	while tweetNeeded > newTweet:
		print ("Je dois envoyer "+str(tweetNeeded)+" / "+str(newTweet))
		with open("TweetsBase.txt") as baseDeTweets:
			ligne = baseDeTweets.readlines()
			random_int = random.randint(0,len(ligne)-1)
		
		print (ligne[random_int])
		api.update_status(ligne[random_int])
		newTweet += 1
		print ("Nouveaux Tweets "+str(newTweet))
		time.sleep(tmpRechargeTweet)
	print("C'est bon on a le compte")


if tweetNeeded > 0:
	EnvoieUnTweet()
