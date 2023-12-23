import string
import numpy as np

class Artist:
    """Class that finds and holds information on a musical artist with a 
    Spotify or RateYourMusic (RYM) page specified by 'url'.""" 
    def __init__(self, url, RYM_interface, spotify_interface):
        self.RYM_interface = RYM_interface
        self.spotify_interface = spotify_interface

        self.RYM_url = None
        self.spotify_url = None
        self.id = None
        self.name = None
        self.current_location = ''
        self.genres = None
        self.mean_rating = 0
        self.works = None
        self.RYM_followers = 0
        self.spotify_followers = None
        
        if 'rateyourmusic' in url:
            self.import_RYM_info(url)
            self.import_spotify_info(spotify_interface.url_from_name(self.name, [work['title'] for work in self.works]))
        elif 'spotify' in url: 
            self.import_spotify_info(url)
        else: raise ValueError('The url provided must be for either a RateYourMusic or Spotify artist page.')

    def import_RYM_info(self, url):
        if not 'rateyourmusic' in url: 
            raise ValueError('The url provided must be for a RateYourMusic artist page.')
        elif url == None: return
        else: self.RYM_url = url
        
        RYM_info = self.RYM_interface.artist_info(self.RYM_url)
        self.name = RYM_info['name']
        self.genres = RYM_info['genres']
        self.works = RYM_info['works']
        self.RYM_followers = RYM_info['followers']
        self.current_location = RYM_info['current location']
        self.mean_rating = (np.sum([work['num ratings'] * work['rating'] for work in self.works]) 
                            / (np.sum([work['num ratings'] for work in self.works])+1e-100))

    def import_spotify_info(self, url):
        if url == None: return
        self.spotify_url = url
        self.id = self.spotify_interface.id_from_url(url)
        if self.id == None: return
        if self.genres == None or self.genres == []: self.genres = [string.capwords(genre) for genre in self.spotify_interface.get_genres(self.id)]
        if self.name == None: self.name = self.spotify_interface.get_name(self.id)
        if self.works == None: self.works = self.spotify_interface.get_works(self.id)
        self.spotify_followers = self.spotify_interface.get_spotify_followers(self.id)

    def print_info(self):
        print(f'\nName: {self.name}')
        print(f'Current Location: {self.current_location}')
        print(f'Genres: {self.genres}')
        print(f'First Work: {self.works[0]}')
        print(f'Number of RYM followers: {self.RYM_followers}')
        print(f'Spotify url: {self.spotify_url}')
        print(f'RYM url: {self.RYM_url}')
        print('\n')

    def horizontal_info(self):
        header = (
            'name' + '\t'
            + 'genres' + '\t'
            + '# Spotify followers' + '\t'
            + '# RYM followers' + '\t'
            + 'mean RYM rating' + '\t'
            + 'current location' + '\t'
            + 'RYM url' + '\t'
            + 'Spotify url'
        )

        info = (
            self.name + '\t'
            + ', '.join(self.genres) + '\t'
            + str(self.spotify_followers) + '\t'
            + str(self.RYM_followers) + '\t'
            + str(round(self.mean_rating,2)) + '\t'
            + self.current_location + '\t'
            + str(self.RYM_url) + '\t'
            + str(self.spotify_url)
        )

        return header, info
        
        