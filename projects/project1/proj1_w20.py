#########################################
##### Name: Chloe Hull              #####
##### Uniqname: hullcm              #####
#########################################

import requests
import json
import webbrowser

class Media:
    '''A type of media from iTunes!

    Attributes
    ----------
    title: string
        The title of the media
    author: string
        The author of the media
    release_year: integer
        The release year of the media
    url: string
        The URL of the media

    '''
    def __init__(self, title="No Title", author="No Author",
    release_year="No Release Year", url="No URL", json=None):
        if (json is None):
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
        else:
            if json['wrapperType'] == 'track':
                self.title = json['trackName']
                self.url = json['trackViewUrl']
            else:
                self.title = json['collectionName']
                self.url = json['collectionViewUrl']

            self.author = json['artistName']
            self.release_year = json['releaseDate'][:4]


    def info(self):
        '''Returns information on the type of media, such as the title,
        author and release year of the media.

        Parameters
        -----------
        none

        Returns
        --------
        str
            The information on the media.

        '''
        release_yr = str(self.release_year)
        media_info = self.title + ' by ' + self.author + " (" + release_yr + ")"
        return media_info


    def length(self):
        '''Returns the length of the media.

        Parameters
        -----------
        none

        Returns
        --------
        int
            The length of the media

        '''
        return 0


class Song(Media):
    '''A song from iTunes!

    Attributes
    ----------
    title: string
        The title of the song
    author: string
        The author of the song
    release_year: integer
        The release year of the song
    url: string
        The URL of the song
    album: string
        The album on which the song appears
    genre: string
        The genre of music under which the song falls
    track_length: integer
        The length of the track
    '''

    def __init__(self, title="No Title", author="No Author",
    release_year="No Release Year", url="No URL", album="No Album",
    genre="No Genre", track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)

        if (json is None):
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.album = json['collectionName']
            self.genre = json['primaryGenreName']
            self.track_length = json['trackTimeMillis']


    def info(self):
        '''Returns information on the song, such as the title,
        author, release year, and genre of the song.

        Parameters
        -----------
        none

        Returns
        --------
        str
            The information on the song.

        '''
        return super().info() + ' [' + self.genre + ']'


    def length(self):
        '''Returns the length of the song.

        Parameters
        -----------
        none

        Returns
        --------
        int
            The length of the song in seconds

        '''
        return super().length() + self.track_length//1000


class Movie(Media):
    '''A movie from iTunes!

    Attributes
    ----------
    title: string
        The title of the movie
    author: string
        The author of the movie
    release_year: integer
        The release year of the movie
    url: string
        The URL of the movie
    rating: string
        The rating of the movie
    movie_length: integer
        The length of the movie
    '''

    def __init__(self, title="No Title", author="No Author",
    release_year="No Release Year", url="No URL", rating="No Rating",
    movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)

        if (json is None):
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.rating = json['contentAdvisoryRating']
            self.movie_length = json['trackTimeMillis']


    def info(self):
        '''Returns information on the movie, such as the title, author,
        release year, and rating of the movie.

        Parameters
        -----------
        none

        Returns
        --------
        str
            The information on the movie.

        '''
        return super().info() + ' [' + self.rating + ']'


    def length(self):
        '''Returns the length of the movie.

        Parameters
        -----------
        none

        Returns
        --------
        int
            The length of the movie in minutes

        '''
        return super().length() + self.movie_length//60000


# Other classes, functions, etc. should go here

BASE_URL = "https://itunes.apple.com/search"


def get_data(url, params=None):
    '''Calls API given a valid API link and returns the json
    representation of the data.

    Parameters
    -----------
    url: str
        The base URL of the API to be called
    params: str
        The terms to be searched for in the API call

    Returns
    --------
    dict
        The results of the API call represented in a dictionary.

    '''
    resp = requests.get(BASE_URL, params = params).json()
    if resp['resultCount'] == 0:
        print("There are no results for this search.")
        exit()
    else:
        return resp


def parse_data(data):
    '''Parses through a dictionary of all data called from the API. Returns
    the relevant data and categorizes each object into the correct media
    type: song, movie, or other media.

    Parameters
    -----------
    data: dict
        The data to be parsed, cleaned, and categorized

    Returns
    --------
    dict
        A dictionary with key-value pairs for songs, movies, and other media

    '''
    songs_list = []
    movies_list = []
    other_list = []
    final_dict = {}
    for key, value in data.items():
        if key == 'results':
            for item in value:
                for key, value in item.items():
                    if key == 'kind' and value == 'song':
                        new_item = Song(json=item)
                        songs_list.append(new_item)
                    elif key == 'kind' and value == 'feature-movie':
                        new_m_item = Movie(json=item)
                        movies_list.append(new_m_item)
                    elif key == 'kind':
                        new_o_list = Media(json=item)
                        other_list.append(new_o_list)
            final_dict['song'] = songs_list
            final_dict['movie'] = movies_list
            final_dict['other'] = other_list
            return final_dict


def print_final(data):
    '''Takes the dictionary of key-value pairs for each category (song,
    movie, and other media), loops through each key-value pair and through
    each item in the value's list, then prints the relevant information
    for each item. While looping through each item, also adds the URL
    representation for each individual item to a dictionary.

    Parameters
    -----------
    data: dict
        The data to be parsed, cleaned, and categorized

    Returns
    --------
    dict
        A dictionary containing the URL for each printed item

    '''
    url_dict = {}
    count = 0
    for key, value in data.items():
        if key == 'song':
            print(' ')
            print("SONGS")
            for item in value:
                count += 1
                formatted_item = str(count) + " " + item.info()
                url_dict[str(count)] = item.url
                print(formatted_item)
        elif key == 'movie':
            print("\n" "MOVIES")
            for item in value:
                count += 1
                formatted_movie = str(count) + " " + item.info()
                url_dict[str(count)] = item.url
                print(formatted_movie)
        else:
            print("\n" "OTHERS MEDIA ")
            for item in value:
                count += 1
                formatted_other = str(count) + " " + item.info()
                url_dict[str(count)] = item.url
                print(formatted_other)
        print(' ')
    return url_dict


### Question 3 Object Creation, commenting out so final program (part 4) runs correctly

# q3_test1 = "term=oh+wonder"
# q3_test2 = 'term=friends'

# q3_tests = [q3_test1, q3_test2]

# for test in q3_tests:
#     data = get_data(BASE_URL, test)
#     data = parse_data(data)
#     print_final(data)

### End of Question 3 Object Creation

if __name__ == "__main__":

    params = None
    while params == None:
        params = input("Enter a search term, or 'exit' to quit: ")

    if params.lower() == 'exit':
        exit()
    else:
        terms = 'term=' + params + ''
        data = get_data(BASE_URL, terms)
        data = parse_data(data)
        url_data = print_final(data)

    params2 = input("Enter a number for a preview of that item, or another search term, or exit: ")
    while params2.lower() != 'exit':
        if params2.isnumeric() and int(params2) < 51:
            terms = 'term=' + params + ''
            URL_search = url_data[str(params2)]
            print(URL_search)
            webbrowser.open(URL_search)
            break
        elif params2.isnumeric() and int(params2) > 51:
            print('That is not a valid number. Try again')
            params2 = input("Enter a number for a preview of that item, or another search term, or exit: ")
        else:
            terms = 'term=' + params2 + ''
            data = get_data(BASE_URL, terms)
            data = parse_data(data)
            url_data = print_final(data)
            params2 = input("Enter a number for a preview of that item, or another search term, or exit: ")
    while params2.lower() == 'exit':
        print('Bye!')
        exit()