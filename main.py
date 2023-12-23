import artist
import RYM_interface
import spotify_interface


""" Takes a set of RYM and/or Spotify Profile URLs and returns dense info. When possible, use RYM URLs. """
def infos_from_urls(urls_txt):
    """ Reads a list of URLS from a file into an array."""
    file = open(urls_txt, "r")
    urls = file.read().split("\n")
    urls_new = []
    if '' in urls: urls.remove('')
    for url in urls: 
        if not url[0] == "#": urls_new.append(url.split("#")[0])
    file.close()

    file = open('output.txt', 'w')
    rym = RYM_interface.RYM()
    spotify = spotify_interface.Spotify()

    i=0
    for url in urls:
        header, info = artist.Artist(url, rym, spotify).horizontal_info()
        if (i == 0): 
            print(header)
            file.write(header + '\n')
        print(info)
        file.write(info + '\n')
        i += 1

    rym.exit_browser()

def urls_from_lists(lists_txt):
    file = open(lists_txt, "r")
    urls = file.read().split("\n")
    urls_new = []
    if '' in urls: urls.remove('')
    for url in urls: 
        if not url == '' and not url[0] == "#": urls_new.append(url.split("#")[0])
    urls = urls_new
    file.close()

    file = open('artist_urls.txt', 'w')
    rym = RYM_interface.RYM()
    spotify = spotify_interface.Spotify()

    artist_urls = []
    for url in urls:
        for artist_url in [url] if not 'https://rateyourmusic.com/list/' in url else rym.artists_from_lists([url]):
            if not artist_url in artist_urls: artist_urls.append(artist_url)
    artist_urls.sort()
    for artist_url in artist_urls: file.write(artist_url + '\n')
        
    file.close()
    rym.exit_browser()

# urls_from_lists('artist_lists.txt') #run first
infos_from_urls('artist_urls.txt') #run second