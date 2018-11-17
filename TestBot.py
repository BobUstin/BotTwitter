import tweepy #Tweepy pour jouer avec l'API Twitter
import time #Time pour avoir la date
import csv #CSV pour l'écriture dans un fichier
import re #re pour trouver les mentions

### DATE DE RECHERCHE ###
import datetime
dateToday = datetime.datetime.now()
dateToday.date()
dateToday.day 
dateRecherche = dateToday.replace(day=dateToday.day-2)
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
canIretweet = True 
canIlike = True 
canIfollow = True 
### FIN DE ACTIVATION DES MODULES ###

### SETUP DE LA RECHERCHE ###
tweets_per_query  = 10000 #Nombre de fois que l'api va se lancer
tmpsRecharge = 300
####
new_tweets = 0 #nbre de nouveaux tweets
total_tweets = 0 #nbre de tweet étudiés
new_follow = 0  #nbre de follow demandés (peut être dejà existant)
new_like = 0  #nbre de nouveau like
alreadyRewteeted = 0
####
keywordsList =  ["#concours","jeuconcours", "CONCOURS", "concours"]   #mots clés à rechercher
bannedWords = ["V-bucks","Vbucks", "fortnite", "clé steam aléatoire", "mentionne", "Pour jouer, c'est par ici"]	#mots clés à éviter
retweetWordList =  ["retweet", "#rt", "rt ", "rt&amp;follow", "rt+"]   #mots clés à retweeter
retweetFollowWordList =  ["follow + retweet", "follow + #rt", "follow + rt"]   #mots clés à retweeter+follow seulement
nbreMinRT = 44 #si le tweet à moins que ce nombre, on ne le prend pas en compte
nbreMaxFollow = 1000 #stop si on a eu plus de ce nombre de new follow
nbreMaxdeMentions = 3 #stop si on depasse ce chiffre, le tweet est évité
#### 
c = csv.writer(open("MONFICHIER.csv", "a")) # Fichier où seront écrit les tweets + url + user
c = csv.writer(open("NOTCONTEST.csv", "a")) # Fichier où sont écrit la même chose mais qui ont été refusés par ma vérification
#### FIN DE SETUP ###


#### LANCEMENT DE LA RECHERCHE ###
for querry in keywordsList:
	print ("Starting new querry: " + querry)

	if canIretweet == False:
		print ("Retweets désactivés")
	else:
		print ("Retweets ACTIVES")

	if canIlike == False:
		print ("Like désactivés")
	else:
		print ("Like ACTIVES")

	if canIfollow == False:
		print ("Follow désactivés")
	else:
		print ("Follow ACTIVES")
####
for tweet in tweepy.Cursor(api.search,
						   q=querry+" -filter=retweets",
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
			total_tweets += 1
			keywordFinded = False
			bannedWordFinded = False
			retweetWordFinded = False
			retweetFollowWordFinded = False
			nbMinRTok = False
			nbreMaxFollowok = False
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

			if new_follow <= nbreMaxFollow:
				nbreMaxFollowok = True
				print("OK - On peut encore follow car seulement : "+str(new_follow))
			else:
				print("FAILED - Trop de new follow pour cette requête: "+str(new_follow))

			if tweet.retweet_count > 44:
				try:
					for screenname in tweet.retweeted_status.entities['user_mentions']:
						nbredeMentions += 1
					else:
						if nbredeMentions <= nbreMaxdeMentions:
							nbreMaxdeMentionsOK = True
							print("OK - Nombre de mentions: "+str(nbredeMentions))
						else:
							print("FAILED - Trop de mentions dans ce tweet: "+str(nbredeMentions))
				except:
					print("erreur au niveau du status retweet")
			if keywordFinded==True and bannedWordFinded == False and nbMinRTok == True and nbreMaxFollowok == True and nbreMaxdeMentionsOK == True:
				for rtfollow in retweetFollowWordList:
					if rtfollow in rechercheText:
						retweetFollowWordFinded = True
						print("RT+Follow trouvé grace à: "+rtfollow)
				else:
					if retweetFollowWordFinded == False:
						print("Ce n'est pas un RT+Follow")	

				for rtonly in retweetWordList:
					if rtonly in rechercheText:
						print("RT Full Loop trouvé grace à: "+rtonly)
						retweetWordFinded = True
				
				else:
					if retweetWordFinded == False:
						print("On ne demande pas de retweet Full Loop")

			else:
				print("Pas un Contest")


			# On lance le script ! RT+Follow ONlY
			if retweetFollowWordFinded==True:
				print("Nbre de retweet pour ce message: "+str(tweet.retweet_count))
				try:
					if canIretweet == True and canIfollow == True:
						tweet.retweet()
						api.create_friendship(tweet.retweeted_status.user.screen_name)
					#c.writerow([username.encode("utf-8"),url.encode("utf-8"),text.encode("utf-8")])
					print("\tRetweeted et followed: "+tweet.retweeted_status.user.screen_name)
					new_tweets += 1
					new_follow += 1

					#Si on demande de liker 	
					if "like" in text or "aime" in text or "fav" in text:
						try:
							if canIlike == True:
								tweet.favorite()
							print('\t' + "Liked")
							new_like += 1
						except:
							print('\tAlready Liked')
					else:
						print("On ne demande pas de liker")

					print ("Total Retweet pour cette requête "+str(new_tweets))
					time.sleep(tmpsRecharge)

					if new_tweets == 10:
						with open("TweetsBase.txt") as baseDeTweets:
							ligne = baseDeTweets.readlines()
							random_int = random.randint(0,len(ligne)-1)
	
						print (ligne[random_int])
						api.update_status(ligne[random_int])
						time.sleep(600)

				except tweepy.TweepError as e:
					print('\tAlready Retweeted')
					alreadyRewteeted += 1 
					print ("Total Retweet pour cette requête "+str(new_tweets))



			### On lance le gros Retweet full Loop !		
			if retweetWordFinded==True:
				print("Nbre de retweet pour ce message: "+str(tweet.retweet_count))
				try:
					if canIretweet == True:
						tweet.retweet()
						#c.writerow([username.encode("utf-8"),url.encode("utf-8"),text.encode("utf-8")])
					print("\tRetweeted")
					new_tweets += 1


					#Si on demande de liker 	
					if "like" in text or "aime" in text or "fav" in text:
						try:
							if canIlike == True:
								tweet.favorite()
							print('\t' + "Liked")
							new_like += 1
						except:
							print('\tAlready Liked')
					else:
						print("On ne demande pas de liker")
					

					#Si on demande de Follow 
					if "follow" in text or "suivre" in text or "abonnez-vous" in text or "suivez" in text or "#fl" in text:
						if len(tweet.retweeted_status.entities['user_mentions']) == 0:
							try:
								if canIfollow == True:
									api.create_friendship(tweet.retweeted_status.user.screen_name)
								new_follow += 1
								print("Follow Original Twitter: " + tweet.retweeted_status.user.screen_name)
							except:
								print('\tAlready Followed')
						else:
							try:
								if canIfollow == True:
									api.create_friendship(tweet.retweeted_status.user.screen_name)
								for screenname in tweet.retweeted_status.entities['user_mentions']:
									if canIfollow == True:
										api.create_friendship(str(screenname['screen_name']))
									print("Mention user: " + str(screenname['screen_name']))
									new_follow += 1
							except:
								print('\tAlready Followed')
					else:
						print("On ne demande pas de follow")

					print ("DONE - Retweeté avec succes pour un total de reweets: "+str(new_tweets))
					time.sleep(tmpsRecharge)

					if new_tweets == 10:
						with open("TweetsBase.txt") as baseDeTweets:
							ligne = baseDeTweets.readlines()
							random_int = random.randint(0,len(ligne)-1)
	
						print (ligne[random_int])
						api.update_status(ligne[random_int])
						time.sleep(600)
				
				except tweepy.TweepError as e:
					print('\tAlready Retweeted')
					alreadyRewteeted += 1 
					print ("Total Retweet pour cette requête "+str(new_tweets))
	


	except tweepy.TweepError as e:
		print(e.reason)

	except StopIteration:

		break
print ("New Tweets: " + str(new_tweets))
print ("Total checked Tweets: " + str(total_tweets))
print ("New Follow: " + str(new_follow))
print ("New Like: " + str(new_like))
print ("Already Retweeted: " + str(alreadyRewteeted))

