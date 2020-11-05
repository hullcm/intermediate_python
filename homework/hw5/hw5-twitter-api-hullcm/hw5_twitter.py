#########################################
##### Name:   Chloe Hull            #####
##### Uniqname:  hullcm             #####
#########################################

from requests_oauthlib import OAuth1
import json
import requests
import operator
import secrets # file that contains your OAuth credentials

CACHE_FILENAME = "twitter_cache.json"
CACHE_DICT = {}

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)

def test_oauth():
    ''' Helper function that returns an HTTP 200 OK response code and a 
    representation of the requesting user if authentication was 
    successful; returns a 401 status code and an error message if 
    not. Only use this method to test if supplied user credentials are 
    valid. Not used to achieve the goal of this assignment.'''

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(client_key, client_secret, access_token, access_token_secret)
    authentication_state = requests.get(url, auth=auth).json()
    return authentication_state


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    param_strings = []
    joiner = '-'

    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + joiner + joiner.join(param_strings)
    return unique_key


def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of
        a dictionary
    '''
    response = requests.get(baseurl,
                            params=params,
                            auth=oauth)
    results = response.json()
    return results


def make_request_with_cache(baseurl, hashtag, count):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.

    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        The hashtag to search (i.e. “#2020election”)
    count: int
        The number of tweets to retrieve

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    terms = {}
    terms['q'] = hashtag
    terms['count'] = count
 #   print(terms)

    unique_string = construct_unique_key(baseurl, terms)
    if unique_string in CACHE_DICT.keys():
        return CACHE_DICT[unique_string]
    else:
        CACHE_DICT[unique_string] = make_request(baseurl, terms)
        save_cache(CACHE_DICT)
        return CACHE_DICT[unique_string]


def find_most_common_cooccurring_hashtag(tweet_data, hashtag_to_ignore):
    ''' Finds the hashtag that most commonly co-occurs with the hashtag
    queried in make_request_with_cache().

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query
    hashtag_to_ignore: string
        the same hashtag that is queried in make_request_with_cache() 
        (e.g. "#election2020")

    Returns
    -------
    string
        the hashtag that most commonly co-occurs with the hashtag 
        queried in make_request_with_cache()

    '''
    tweet_data = tweet_data['statuses']
    hashtags = {}
    for item in tweet_data:
        tags = []
        if 'RT @' not in item['text']:
            tags_list = item['entities']['hashtags']
            for item in tags_list:
                tags.append(item['text'].lower())
            for item in tags:
                if item in hashtags.keys():
                    hashtags[item] += 1
                else:
                    hashtags[item] = 1

    del hashtags[hashtag_to_ignore[1:]]
    most_common_hash = max(hashtags.items(), key=operator.itemgetter(1))[0]
    return most_common_hash


if __name__ == "__main__":
    if not client_key or not client_secret:
        print("You need to fill in CLIENT_KEY and CLIENT_SECRET in secret_data.py.")
        exit()
    if not access_token or not access_token_secret:
        print("You need to fill in ACCESS_TOKEN and ACCESS_TOKEN_SECRET in secret_data.py.")
        exit()

    CACHE_DICT = open_cache()
    baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    hashtag = "#2020election"
    count = 100

    tweet_data = make_request_with_cache(baseurl, hashtag, count)
    most_common_cooccurring_hashtag = find_most_common_cooccurring_hashtag(tweet_data, hashtag)
    print("The most commonly cooccurring hashtag with {} is {}.".format(hashtag, most_common_cooccurring_hashtag))
