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
    
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):
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
        '''Returns information on the type of media, such as the title, author
        and release year of the media.
        
        Parameters
        -----------
        none

        Returns
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
        int
            The length of the media
        '''
        return 0


class Song(Media):
    '''A song from iTunes!
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
    album: string
        The album the song is from
    genre: string
        The genre of music the song falls under
    track_length: integer
        The length of the track 
    '''

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album="No Album", genre="No Genre", track_length=0, json=None):
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
        '''Returns information on the song, such as the title, author,
        release year, and genre of the media.
        
        Parameters
        -----------
        none

        Returns
        str
            The information on the media.
        '''
        return super().info() + ' [' + self.genre + ']'
    
    def length(self):
        '''Returns the length of the song.
        
        Parameters
        -----------
        none

        Returns
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

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating="No Rating", movie_length=0, json=None):
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
        int
            The length of the movie in minutes
        '''
        return super().length() + self.movie_length//60000

# Other classes, functions, etc. should go here

BASE_URL = "https://itunes.apple.com/search" ### Does this need to go somewhere else bc its a global variable?

def get_data(url, params=None):
    '''ADD DOCSTRING
    '''
    resp = requests.get(BASE_URL, params = params).json()
    return resp

def parse_data(data):
    '''ADD DOCSTRING
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
                        new_item = Song(json=item).info()
                        songs_list.append(new_item)
                    elif key == 'kind' and value == 'movie':
                        new_m_item = Movie(json=item).info()
                        movies_list.append(new_m_item)
                    elif key == 'kind':
                        new_o_list = Media(json=item).info()
                        other_list.append(new_o_list)
            final_dict['song'] = songs_list
            final_dict['movie'] = movies_list
            final_dict['other'] = other_list
            return final_dict

def format_data(data):
    '''ADD DOCSTRING
    '''
    final_songs_list = ['SONGS']
    final_movies_list = ['\n''MOVIES \n']
    final_others_list = ['OTHER \n']

    count = 0
    for key, value in data.items():
        if key == 'song':
            for item in value: 
                count += 1
                formatted_song = str(count) + " " + item
                final_songs_list.append(formatted_song)
        elif key == 'movie':
            for item in value:
                count += 1
                formatted_movie = str(count) + " " + item
                final_movies_list.append(formatted_movie)
        else:
            for item in value:
                count += 1
                formatted_other = str(count) + " " + item + "\n"
                final_others_list.append(formatted_other)
    return final_songs_list, final_movies_list, final_others_list

def final_print(data):
    '''ADD DOCSTRING
    '''
    print(data)
    for item in data:
        for item in item:
            print(item.info(), item.url) ### review this 

### Question 3 Object Creation

def present_data(BASE_URL, params):
    '''ADD DOC
    '''
    data = get_data(BASE_URL, params)
    data = parse_data(data)
    print(data)
 #   data = format_data(data)
  #  data = final_print(data)
    return data

def get_url(BASE_URL, params, index):
    '''ADD DOC
    '''
    url_info = ''
    data = get_data(BASE_URL, params)
    data = parse_data(data)
    data = format_data(data)
   # print(data) ### HAVE TO FIGURE OUT HOW TO GET IT TO PULL UP THE RIGHT PREVIEW
    url_info = data[int(index)]['trackViewUrl']
    return url_info

if __name__ == "__main__":

    params = None
    while params == None:
        params = input("Enter a search term, or 'exit' to quit: ")
    terms = 'term=' + params + ''
    present_data(BASE_URL, terms)
    
    params2 = input("Enter a number for more info, or another search term, or exit: ")
    while params2 == 'exit':
        print('Bye!')
        exit()
    if params2.isnumeric():
        terms = 'term=' + params + ''
        URL_search = get_url(BASE_URL, terms, params2)
        print(URL_search)
        webbrowser.open(URL_search)
        break
    while params2 is str and params2 != 'exit': #### figure out how to make this work
        terms = 'term=' + params + ''
        present_data(BASE_URL, terms)
        params2 = input("Enter a number for more info, or another search term, or exit: ")
    