import requests
from os import environ as ENV

def query_twitter():
    print ("query twitter")
    bearer_token = ENV.get('TWITTER_BEARER_TOKEN')
    r = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json?q=pagerduty%20%20OR%20%23pdsummit%20OR%20pagerdutysummit',
        headers = {'authorization': f'Bearer {bearer_token}'}
        )
    return r.json()['statuses'

