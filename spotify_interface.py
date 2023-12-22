import os
import base64
from dotenv import load_dotenv
from requests import post, get
import json
import util

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

    """ Returns the Spotify 'artist_id' for a particular artist. As there may be multiple artists with a 
        particular 'artist_name', this method determines the correct artist by comparing their known 'works' (e.g.,
        albums, singles, EPs) to the Spotify titles for each artist. """
    def get_artist_id_from_name(self, artist_name, works):
        url = "https://api.spotify.com/v1/search"
        is_page_empty = False
        increment = 0
        while not is_page_empty and increment < 20: #while there are still results coming in, increment the page...
            query = f"?q={artist_name}&type=artist&limit=50&offset=" + str(increment*50)
            query_url = url + query
            result = get(query_url, headers=self.auth_header)
            json_result = json.loads(result.content)
            for result in json_result["artists"]["items"]:
                if (util.string_simplify(artist_name) == util.string_simplify(result["name"])):
                    this_artist_works = self.get_artist_works(result["id"])
                    do_works_overlap = len(set(util.strings_simplify(works)).intersection(set(util.strings_simplify(this_artist_works)))) > 0
                    if (do_works_overlap): return result["id"]
            increment += 1
            if len(json_result["artists"]["items"]) == 0: is_page_empty = True;
        return None

    """ Returns the Spotify 'artist_id' for a particular artist. As there may be multiple artists with a 
            particular 'artist_name', this method determines the correct artist by comparing their known 'works' (e.g.,
            albums, singles, EPs) to the Spotify titles for each artist. """

    def get_artist_id_from_url(self, spotify_url):
        if 'https://open.spotify.com/artist/' in spotify_url: return spotify_url.split("/artist/")[1]
        return None

    """ Returns the artist genres given their Spotify 'artist_id'. """
    def get_artist_genres(self, artist_id):
        if artist_id == None: return None
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        return json.loads(get(url, headers=self.auth_header).content)['genres']

    """ Returns the artist name given their Spotify 'artist_id'. """
    def get_artist_name(self, artist_id):
        if artist_id == None: return None
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        return json.loads(get(url, headers=self.auth_header).content)['name']

    """ Returns the names of all works of an artist given their Spotify 'artist_id'. """
    def get_artist_works(self, artist_id):
        if artist_id == None: return None
        albums = []
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        json_result = json.loads(get(url, headers=self.auth_header).content)["items"]
        for result in json_result: albums.append(util.string_simplify(result["name"]))
        return albums

    """ Returns the number of Spotify followers for a particular artist with Spotify 'artist_id'. """
    def get_spotify_followers(self, artist_id):
        if artist_id == None: return None
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        result = get(url, headers=self.auth_header)
        json_result = json.loads(result.content)
        return json_result["followers"]["total"]

    """ Returns the Spotify url for a particular artist with Spotify 'artist_id'. """
    def get_spotify_url(self, artist_id):
        if artist_id == None: return None
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        result = get(url, headers=self.auth_header)
        json_result = json.loads(result.content)
        return json_result["external_urls"]["spotify"]