import requests
import os
import json
import pandas as pd

os.environ['TOKEN'] = "AAAAAAAAAAAAAAAAAAAAANeeVwEAAAAA9r%2F24zezZtHKDdz4uFFxDUAVGe0%3DZlO2pvkzMNbKX4NJKBAxtQogA4dKkVztFjptNhxqLkSbiZnLp5"


def auth():
    return os.getenv('TOKEN')


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(keyword, start_date, end_date, max_results=10):

    # Change to the endpoint you want to collect data from
    search_url = "https://api.twitter.com/2/tweets/search/all"

    # change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'next_token': {}}

    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token=None):
    # params object received from create_url function
    params['next_token'] = next_token
    response = requests.request("GET", url, headers=headers, params=params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


if __name__ == "__main__":

    bearer_token = auth()
    headers = create_headers(bearer_token)
    keyword = "(COVID OR COIVD-19 OR covid OR covid-19 OR #COVID OR #COIVD-19 OR #covid OR #covid-19 OR coronavirus OR vaccination OR VACCINATION OR #vaccination OR #VACCINATION OR Moderna OR Pfizer OR Janssen OR AstraZeneca) place_country:CA -is:retweet lang:en"
    start_time = "2021-11-19T23:10:00.000Z"
    end_time = "2021-11-20T23:00:00.000Z"
    max_results = 100

    url = create_url(keyword, start_time, end_time, max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1])    
    result = []
    for response in json_response["data"]:
        tweet_text = response["text"]        
        tweet_text = tweet_text.replace("\n", " ")
        result.append({'tweet_id': response["id"],
                      'tweet_text': tweet_text})
       
df = pd.DataFrame(result)
df.to_csv('100_tweets_19.csv', index=False)
print("file created successfully, lines added ", df.size)

