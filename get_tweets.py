import tweepy
from tweepy import TweepError, RateLimitError

consumer_key = 'RCTWX5r0BO0zyjQ50OS268ncR'
consumer_secret = 'WI0HvC6l48acFfwHzs2cdNPIDOX7GGd7mpqGJp6gj91leqaz2a'
access_token = '1147242589763985408-NRlVMq7EhFJD8dP2Y2RTwBtdkPtueu'
access_token_secret = 'aOrlhXbs8o8MNHwxCtml7jyHwpW3UyTMzL7pQ5Zqd92oB'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
data = None
with open('election-day.txt', 'r') as file:
    data = file.read().split('\n')
data = data[360000:]
with open('tweet-text.txt', 'a', encoding='utf-8') as tweet_file:
    for id in range(900, 1801):
        tweet = None
        try:
            tweet = api.get_status(data[id])
        except RateLimitError:
            print("Rate limited, stopped. Continue in 15 mins.")
            break
        except TweepError as e:
            if e.api_code == 144:
                print("Tweet doesn't exist. Skipping.")
                continue
            elif e.api_code != 88:
                print("Error with tweet ID, skipping.")
                continue
            else:
                print(e.response)
                break
        if tweet.lang == "en" and tweet.truncated == False:
            print(tweet.id)
            text = tweet.text.strip('\n')
            text = text.strip('\t')
            text = text.replace('\n', '')
            text = text.replace('\t', '')
            tweet_file.write(text + "\n")
