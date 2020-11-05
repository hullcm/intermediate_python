#################################
##### Name: Chloe Hull
##### Uniqname: hullcm
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key

CACHE_FILENAME = 'site_cache.json'

class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, name, category, address, zipcode, phone, url=None):
        self.name = name
        self.category = category
        self.address = address
        self.zipcode = zipcode
        self.phone = phone

    def info(self):
        '''Returns a string representation of the relevant information for
        the national park

        Parameters
        -----------
        none

        Returns
        ---------
        str
            the properly formatted string representation of the national park
        '''
        site_info = self.name + ' (' + self.category + ')' + ': ' + self.address + ' ' + self.zipcode
        return site_info


def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    state_url_dict = {}
    #Make the soup
    url = 'https://www.nps.gov/index.htm'
    response = make_request_with_cache(url)
    soup = BeautifulSoup(response, 'html.parser')

    # Get the states div
    states = soup.find('ul', class_="dropdown-menu SearchBar-keywordSearch")

    # get the list items
    list_states = states.find_all('li')

    # extract state name & URL & create dictionary
    for state in list_states:
        name = state.find('a').text.lower()
        url = state.find('a')['href']
        state_url_dict[name] = url

    # edit URL in dict
    for key, value in state_url_dict.items():
        state_url_dict[key] = 'https://www.nps.gov' + value
    return state_url_dict


def get_site_instance(site_url):
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''
    # make the soup
    response = make_request_with_cache(site_url)
    soup = BeautifulSoup(response, 'html.parser')

    # get park name
    name = soup.find('a', class_="Hero-title").text

    # get category
    category = soup.find('span', class_='Hero-designation').text

    # get address
    address = soup.find('div', class_='mailing-address')
    state = address.find('span', itemprop='addressRegion').text
    city = address.find('span', itemprop='addressLocality').text
    final_address = city + ', ' + state

    #get zip
    zipcode = address.find('span', itemprop='postalCode').text.strip()

    # get phone
    phone = soup.find('div', class_='vcard')
    phone = phone.find('span', itemprop='telephone').text.strip()

    # get national site instance, properly formatted
    site_instance = NationalSite(name, category, final_address, zipcode, phone)
    return site_instance


def get_state_url():
    '''Generates the url for the user's desired state

    Parameters
    ----------
    None

    Returns
    --------
    str
        the url for the desired state
    '''
    url_dict = build_state_url_dict()
    state = input('Enter a state name (eg. Michigan, michigan) or "exit": ').lower()
    while state != 'exit':
        while state not in url_dict.keys():
            print('[ERROR]: That is not a valid state. Please try again')
            state = input('Enter a state name (eg. Michigan, michigan) or "exit": ').lower()
            if state == 'exit':
                exit()
        else:
            return url_dict[state]
    exit()


def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances
    '''
    # make the soup
    response = make_request_with_cache(state_url)
    soup = BeautifulSoup(response, 'html.parser')

    #identify state 
    state_name = soup.find('h1', class_='page-title').text

    # get the list that contains all national sites
    site_listing_parent = soup.find('ul', id='list_parks')
    site_listing_lis = site_listing_parent.find_all('li', class_='clearfix')
    count = 1
    site_listings = []
    listing_to_print = []
    for site_listing_li in site_listing_lis:

        # go through each site div & extract the URL for the site details page
        site_link_tag = site_listing_li.find('h3')
        site_link_tag = site_link_tag.find('a')
        site_link_path = site_link_tag['href']
        site_link_url = 'https://www.nps.gov/' + site_link_path + 'index.htm'

        # crawl to the details of each page & extract relevant info
        site_instance = get_site_instance(site_link_url)
        site_listings.append(site_instance)

    # print relevant info
        formatted_site_info = site_instance.info()
        listing_to_print.append('[' + str(count) + '] ' + formatted_site_info)
        count += 1

        # get state name for printing
    print('---------------------------------')
    print('List of national sites in', state_name)
    print('---------------------------------')
    for item in listing_to_print:
        print(item)
    return site_listings


def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    map_url = 'http://www.mapquestapi.com/search/v2/radius'
    site = site_object
    site_name = site.name
    site_zip = site.zipcode

    params = {'key': secrets.API_KEY, 'origin': site_zip, 'radius': 10, 'maxMatches': 10, 'ambiguities': 'ignore', 'outFormat': 'json'}
    response = make_request_with_cache(map_url, params = params)

    for item in response['searchResults']:
        for key, value in item.items():
            new_dict = {}
            if key == 'name':
                name = value
            if key == 'fields':
                for key, value in value.items():
                    if key == 'group_sic_code_name':
                        if value == '':
                            category = 'no category'
                        else:
                            category = value
                    if key == 'address':
                        if value == '':
                            address = 'no address'
                        else:
                            address = value
                    if key == 'city':
                        if value == '':
                            city = 'no city'
                        else:
                            city = value
        print_value = '- ' + name + ' (' + category + '): ' + address + ', ' + city
        print(print_value)
    return response


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache
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
    ''' saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    fw = open(CACHE_FILENAME,"w")
    fw.write(json.dumps(cache_dict))
    fw.close()


def make_request(url, params=None):
    '''Makes an api request with params if they exist, 
    otherwise with just the base url

    Parameters
    -----------
    url: str
        url for the API to be called
    params: dict
        parameters for the API call

    Returns
    -------
    str
        the text results from the API call
    '''

    if params != None:
        response = requests.get(url, params = params)
        final_response = response.json()
    else:
        response = requests.get(url)
        final_response = response.text
    return final_response


def make_request_with_cache(url, params=None):
    '''Makes an api request if request is not stored in the cache
    
    Parameters
    -----------
    url: str
        url for the API to be called
    params: dict
        parameters for the API call

    Returns
    -------
    str
        the text results from the API call
    '''
    if params != None:
        zcode = params['origin']
        url_to_store = url + zcode
        if url_to_store in CACHE_DICT:
            print('Using Cache')
            return CACHE_DICT[url_to_store]
        else:
            print('Fetching')
            CACHE_DICT[url_to_store] = make_request(url, params = params) ### this is how i made caching work
            save_cache(CACHE_DICT)
            return CACHE_DICT[url_to_store]
    else:
        if url in CACHE_DICT:
            print('Using Cache')
            return CACHE_DICT[url]
        else:
            print('Fetching')
            url = url
            CACHE_DICT[url] = make_request(url) ### this is how i made caching work
            save_cache(CACHE_DICT)
            return CACHE_DICT[url]


CACHE_DICT = open_cache()

if __name__ == "__main__":
    url = get_state_url()
    states = get_sites_for_state(url)
    next_search = input('Choose the number for detailed search, back to search another state, or exit: ')
    while next_search.lower() != 'exit':
        while next_search.lower() == 'back':
            url = get_state_url()
            states = get_sites_for_state(url)
            next_search = input('Choose the number for detailed search, back to search another state, or exit: ')
        while next_search.isnumeric():
            index_value = int(next_search) - 1
            try:
                search_obj = states[index_value]
                print('-------------------------')
                place_name = search_obj.name
                print(' Places near', place_name)
                print('-------------------------')
                get_nearby_places(search_obj)
                print(' ')
                next_search = input('Choose the number for detailed search, back to search another state, or exit: ')
            except: 
                next_search = input('That is not a valid number. Select a valid number for detail, back to search another state, or exit: ')
        if next_search != 'back' and next_search != 'exit':
            next_search = input('[ERROR]: That is not a valid entry. Choose a number for detailed search, back to search another state, or exit: ')

    exit()