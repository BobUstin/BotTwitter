import tweepy #Tweepy pour jouer avec l'API Twitter
import time #Time pour avoir la date
import csv #CSV pour l'écriture dans un fichier
import re #re pour trouver les mentions

### DATE DE RECHERCHE ###
import datetime
dateToday = datetime.datetime.now()
dateToday.date()
dateToday.day 
dateRecherche = dateToday.replace(year=dateToday.year-2)
print (dateRecherche.date())
### FIN DATE DE RECHERCHE ###

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

### ACTIVATION DES MODULES ###

### FIN DE ACTIVATION DES MODULES ###
def EnvoieUnRETweet():
	### SETUP DE LA RECHERCHE ###
	tweets_per_query  = 10000 #Nombre de fois que l'api va se lancer
	tmpsRechargeBonRetweet = 240
	####
	new_tweets_registered = 0 #nbre de nouveaux tweets
	total_tweets_studied = 0 #nbre de tweet étudiés
	retweetNeeded = 90  #nbre de retweet needed pour cette request
	####
	keywordsList =  ["gameone", "wwf", "#fanart", "blizzard","#voyage"]   #mots clés à rechercher
	bannedWords = ["retweet", "#rt", "rt ", "rt&amp;follow", "rt+", "follow + retweet", "follow + #rt", "follow + rt"]	#mots clés à éviter
	nbreMinRT = 5 #si le tweet à moins que ce nombre, on ne le prend pas en compte
	nbreMaxdeMentions = 2 #stop si on depasse ce chiffre, le tweet est évité
	#### 
	canIgetTweets = True 
	alreadyRewteeted = 0
	#### FIN DE SETUP ###

	#### LANCEMENT DE LA RECHERCHE ###



	for querry in keywordsList:
		print ("Starting new querry: " + querry)

	####
	for tweet in tweepy.Cursor(api.search,
							   q=querry+" -filter=retweets",lang="fr",
							   since = dateRecherche.date(),
							   tweet_mode="extended").items(tweets_per_query):
	####
		try:
			#Récupération du tweet
			tweetId = tweet.user.id
			username = tweet.user.screen_name
			id = tweet.id
			print ('\n\nFound tweet by: @'+username)
			url = 'https://twitter.com/' + username +  '/status/' + str(id)
			print (url)
			total_tweets_studied += 1
			keywordFinded = False
			bannedWordFinded = False
			
			nbMinRTok = False

			nbreMaxdeMentionsOK = False
			nbredeMentions = 0
			#Vérification si c'est bien l'original et non pas un RT
			try:
				text = tweet.retweeted_status.full_text.lower()
			except:
				text = tweet.full_text.lower()
			print (text)

			#Vérification des mots clés
			rechercheText = text.lower()

			for keyword in keywordsList:
				if keyword in rechercheText:
					keywordFinded = True
					print("OK - KEYword trouvé : "+keyword)	
				else:
					print("FAILED - KEYword manquant")

			for bannedword in bannedWords:
				if bannedword in rechercheText:
					bannedWordFinded = True
					print("FAILED - BANNEDword trouvé: "+bannedword)	
			else:
				print("OK - Fin du check des BANNEDwords")

			if tweet.retweet_count > nbreMinRT:
				nbMinRTok = True
				print("OK - Nombre de retweet : "+str(tweet.retweet_count))
			else:
				print("FAILED - pas assez de retweet "+str(tweet.retweet_count)+" / "+str(nbreMinRT))

			if new_tweets_registered < retweetNeeded:
				print("On peut retweeter encore "+str(new_tweets_registered)+" / "+str(retweetNeeded))
			else:
				canIgetTweets = False
				print("On a assez de retweet "+str(new_tweets_registered)+" / "+str(retweetNeeded))
				break

			if keywordFinded==True and bannedWordFinded == False and nbMinRTok == True and canIgetTweets == True:
				print("On peut retweeter"+text)
				try:
					tweet.retweet()
					new_tweets_registered += 1
					print('\tEt on a retweeté')
					time.sleep(tmpsRechargeBonRetweet)
				except tweepy.TweepError as e:
						alreadyRewteeted += 1 
						print('\tAlready Retweeted')
						
			else:
				print("Pas un bon tweet")

			
		except tweepy.TweepError as e:
			print(e.reason)

		except StopIteration:
			break

	print ("New Tweets: " + str(new_tweets_registered))
	print ("Total checked Tweets: " + str(total_tweets_studied))

EnvoieUnRETweet()