from twitter import *
from datetime import datetime, timedelta
import time
import csv
import sys

def getGender(name):

    trimmedName = (name.partition(' ')[0]).lower()

    file_female = open("female_names.csv", "r")
    bigString_female = file_female.read()
    femaleNames = bigString_female.split(',')

    file_male = open("male_names.csv", "r")
    bigString_male = file_male.read()
    maleNames = bigString_male.split(',')



    for femaleName in femaleNames:
        if trimmedName == femaleName.lower():
            return "female"

    for maleName in maleNames:
        if trimmedName == maleName.lower():
            return "male"

    return "none"

#authentication for the twitter api
t = Twitter(
    auth=OAuth('1104710748968755201-AqUjzBvEZBmKY4fchydoApwx6JueJS', 'pkTTNrKHradYCIeQayPS9c2iU7gMndWgFjVQ6azNf7JQK', '0AiTG8fZVZHX7c7grH5jJ1BCR', 'KLBcoq9vQy60w1PkCvLlavr4w9qMJrA2gO6UN32lgCnU1EqQO8'))

search_hashtag = raw_input("what do you want to search for?")

tweets_bulk =  t.search.tweets(q= search_hashtag, count=100)


#Empty list to hold all tweets
tweets_bulk = []

#Create todays date
d = datetime.today()

print ("Date today", d)

#Perform the API call 10 times, pushing tweets to the list each time
for x in range(7):
    these_tweets = t.search.tweets(q= search_hashtag, result_type='recent', until=d.strftime('%Y-%m-%d'), count=100)
    tweets_bulk.extend(these_tweets['statuses'])
    d = d - timedelta(days=1)
    time.sleep(0.3)
#print tweets_bulk['statuses']

female_count = 0
male_count = 0
country_list = []

country_occurences = {}


print "Number of tweets collected: ", len(tweets_bulk)

for tweet in tweets_bulk:

    #Get the user object from the current tweet
    user = tweet['user']


    if user['location'] != None:
        user_country = user['location']
        if user_country in country_occurences:
            country_occurences[user_country] = country_occurences[user_country] +1
        else:
            country_occurences[user_country]=1


    #Retrieve their name
    name = user['name']

    gender = getGender(name)

#    print 'Gender:', gender, ' name: ', name

    if gender == 'male':
        male_count = male_count + 1

    if gender == 'female':
        female_count = female_count + 1



print "country occurences", country_occurences
#print tweets

print "number of males:", male_count
print "number of females:", female_count
