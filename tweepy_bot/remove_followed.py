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

with open('./names.txt', 'r+') as f:
    for line in f.readlines():
        name = line[:-1]
        try:
            api.destroy_friendship(name)
            print(f'Friend {name} removed')
        except tw.TweepError as e:
            print(f'Friend {name} already removed with error {e}')
open('./names.txt', 'w').close()