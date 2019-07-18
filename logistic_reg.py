import re
from textblob import TextBlob
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import *
content = None

with open('tweet-text.txt', 'r', encoding='utf-8') as file:
    content = [x.strip() for x in file.readlines()]

def process_string(str):
    stemmer = PorterStemmer()
    processed = re.sub("@[\w]*", '', str).lower()  # Remove @users
    processed = re.sub(r'http\S+', '', processed)  # Remove links
    processed = processed.replace("rt : ", "")
    processed = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/ \/ \S+)", " ", processed).split())
    split_processed = processed.split()
    for i, str in enumerate(split_processed):
        split_processed[i] = stemmer.stem(str)
    return ' '.join(split_processed)

for i, string in enumerate(content):
    content[i] = process_string(string)

def bow_extractor(tweets):
    bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
    return bow_vectorizer.fit_transform(tweets)

trump_positive = ['#draintheswamp', '#crookedhillary', '#makeamericagreatagain', '#maga', '#lockherup', '#trumpforpresident']
trump_negative = ['#imwithher', '#nevertrump', '#strongertogether', '#clinton2016']
trump_positive_tweets = []
trump_negative_tweets = []
neutral = []

for i in range(len(content)):
    tweet = content[i]
    polarity = TextBlob(tweet).sentiment.polarity
    if any(x in tweet.lower() for x in trump_positive):
        trump_positive_tweets.append(tweet)
    elif any(x in tweet.lower() for x in trump_negative):
        trump_negative_tweets.append(tweet)
    elif polarity < 0:
        if "trump" or "donald" in tweet.lower():
            trump_negative_tweets.append(tweet)
        elif "clinton" or "hillary" in tweet.lower():
            trump_positive_tweets.append(tweet)
    elif polarity > 0:
        if "trump" or "donald" in tweet.lower():
            trump_positive_tweets.append(tweet)
        elif "clinton" or "hillary" in tweet.lower():
            trump_negative_tweets.append(tweet)
    else:
        neutral.append(tweet)

all_tweets = trump_positive_tweets + trump_negative_tweets + neutral
Y = []
for tweet in all_tweets:
    if tweet in trump_positive_tweets:
        Y.append(1)
    elif tweet in trump_negative_tweets:
        Y.append(-1)
    elif tweet in neutral:
        Y.append(0)

bow_tweets = bow_extractor(all_tweets)
train_X, test_X, train_Y, test_Y = train_test_split(bow_tweets, Y, test_size=0.3, random_state=21)
logRegModel = LogisticRegressionCV(cv=5, max_iter=10000, multi_class='multinomial').fit(train_X, train_Y)
print(logRegModel.score(test_X, test_Y))
# Originall 17, 22

# 859, 601