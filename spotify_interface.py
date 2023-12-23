import os
import base64
from dotenv import load_dotenv
from requests import post, get
import json
import string

class Spotify():
    def __init__(self):
        load_dotenv()
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        auth_string = client_id + ":" + client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {"Authorization": "Basic " + auth_base64, "Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}

        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        self.token = json_result["access_token"]
        self.auth_header = {"Authorization": "Bearer " + self.token}

    """ Simplifies a string by removing excess spaces, removing punctuating, and making lowercase. """
    def string_simplify(self, s): return s.strip().translate(str.maketrans('', '', string.punctuation)).lower()

    """ Simplifies an array of strings by removing excess spaces, removing punctuating, and making lowercase."""
    def strings_simplify(self, s):
        if s == None: return None
        return [self.string_simplify(unsimp) for unsimp in s]

    def get_genres(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        result = get(url, headers=self.auth_header)
        return json.loads(result.content)['genres']

    """ Returns the artist name given their Spotify 'artist_id'. """
    def get_name(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        result = get(url, headers=self.auth_header)
        return json.loads(result.content)['name']

    """ Returns the names of all works of an artist given their Spotify 'artist_id'. """
    def get_works(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        result = get(url, headers=self.auth_header)
        json_result = json.loads(result.content)["items"]
        return [self.string_simplify(result["name"]) for result in json_result]

    """ Returns the number of Spotify followers for a particular artist with Spotify 'artist_id'. """
    def get_spotify_followers(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        result = get(url, headers=self.auth_header)
        json_result = json.loads(result.content)
        return json_result["followers"]["total"]
    
    def id_from_name(self, artist_name, works):
        max_iters = 20
        for i in range(max_iters):
            query_url = "https://api.spotify.com/v1/search" + f"?q={artist_name}&type=artist&limit=50&offset=" + str(i*50)
            result = get(query_url, headers=self.auth_header)
            json_result = json.loads(result.content)
            for result in json_result["artists"]["items"]:
                if (self.string_simplify(artist_name) == self.string_simplify(result["name"])):
                    this_artist_works = self.get_works(result["id"])
                    do_works_overlap = len(set(self.strings_simplify(works)).intersection(set(self.strings_simplify(this_artist_works)))) > 0
                    if (do_works_overlap): return result["id"]
            if len(json_result["artists"]["items"]) == 0: return None

    def id_from_url(self, url):
        if not 'spotify.com/artist/' in url: raise ValueError('You must specifya valid Spotify artist url.')
        return url.split("/artist/")[1].split('?')[0]

    def url_from_name(self, artist_name, works):
        return self.url_from_id(self.id_from_name(artist_name, works))
    
    def url_from_id(self, artist_id):
        if artist_id == None: return None
        return f"https://open.spotify.com/artist/{artist_id}"
    