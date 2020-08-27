import requests
from os import environ as ENV

def query_twitter():
    print ("query twitter")
    bearer_token = ENV.get('TWITTER_BEARER_TOKEN', '123') # Default to 123 to ensure a 401 is returned rather than a 400.
    r = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json?q=pagerduty%20%20OR%20%23pdsummit%20OR%20pagerdutysummit',
        headers = {'authorization': f'Bearer {bearer_token}'}
        )
    if r.status_code == 401:
        print("401 Unauthorized, make sure you've entered the correct Bearer Token.")
    elif r.status_code == 400:
        print("400 Bad Request, make sure that your bearer token is entered.")
    elif r.status_code != 200:
        print("Non-200 response returned!")
        print(r.status_code)
    return r.json()['statuses']

