import os
import tweepy as tw
from dotenv import load_dotenv

load_dotenv()

# authenticate tweepy
auth = tw.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))

api = tw.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authorized")
except:
    print("Auth Error")

def limit_handled(cursor):
    while True:
        try:
            yield next(cursor)
        except tw.RateLimitError:
            time.sleep(15 * 60)


with open('names.txt', 'a+') as f:
    search_words = "#unity3d" + " -filter:retweets"
    date_since = "2021-01-01"
    # Collect tweets
    tweets = limit_handled(tw.Cursor(api.search,
                q=search_words,
                lang="en",
                since=date_since).items())
    # tweets = tw.Cursor(api.search,
    #               q=search_words,
    #               lang="en",
    #               since=date_since).items(5)
    # Iterate and print tweets
    for tweet in tweets:
        try:
            name = tweet.author.screen_name
            api.create_friendship(screen_name = name)
            print(f'Now following {name}')
            f.write(name +'\n')
            
        except tw.TweepError:
            print('Already following')
