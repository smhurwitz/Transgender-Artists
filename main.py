import spotify_interface
import util
import RYM_interface

""" Takes a set of RYM and/or Spotify URLs and returns dense info. When possible, use RYM URLs. """
def get_artist_infos(rym, write_list=False, artist_urls=["https://rateyourmusic.com/artist/my-chemical-romance"]):
    spotify = spotify_interface.Spotify()
    header = "name" + '\t' + "number spotify followers" + '\t' + "total RYM reviews" + '\t' + "mean RYM rating" + '\t' \
             + "max RYM album/EP rating" + '\t' + 'genres' + '\t' + "RYM url" + '\t' + "Spotify url"
    print(header)
    if write_list:
        file = open('output.txt', 'w')
        file.write(header + '\n')

    for artist_url in artist_urls:
        if 'rateyourmusic' in artist_url:
            artist_info = rym.get_RYM_artist_info(artist_url)
            artist_name = artist_info['name']
            total_ratings = artist_info['number of ratings']
            mean_rating = artist_info['mean rating']
            if not mean_rating == None: mean_rating = round(mean_rating, 2)
            max_rating = artist_info['max rating']
            work_titles = rym.get_work_titles(artist_info)
            genres = util.array_to_string(artist_info['genres'])

            artist_id = spotify.get_artist_id_from_name(artist_name, work_titles)
            num_spotify_followers = spotify.get_spotify_followers(artist_id)
            spotify_artist_url = str(spotify.get_spotify_url(artist_id))
            RYM_artist_url = artist_url
        elif 'spotify' in artist_url:
            artist_id = spotify.get_artist_id_from_url(artist_url)
            artist_name = spotify.get_artist_name(artist_id)
            num_spotify_followers = spotify.get_spotify_followers(artist_id)
            genres = util.array_to_string(spotify.get_artist_genres(artist_id))
            spotify_artist_url = str(spotify.get_spotify_url(artist_id))
            total_ratings = 0; mean_rating = 0; max_rating = 0; RYM_artist_url = "";

        info = artist_name + '\t' + str(num_spotify_followers) + '\t' + str(total_ratings) + '\t' + str(
            mean_rating) + '\t' + str(max_rating) + '\t' + genres + '\t' + RYM_artist_url + '\t' + spotify_artist_url
        print(info)
        if write_list: file.write(info + '\n')
    if write_list: file.close()

rym = RYM_interface.RYM()

# rym.get_artists_from_list(True, util.read_urls("rym_artists_lists.txt")) #print list of all artists to .txt file
get_artist_infos(rym, True, util.read_urls("artist_urls_from_custom.txt") + util.read_urls("artist_urls_from_lists.txt")) #final output

# rym.print_artist_info(rym.get_RYM_artist_info("https://rateyourmusic.com/artist/莉犬")) #final output
# spotify = spotify_interface.Spotify()
# print(util.array_to_string(spotify.get_artist_genres(spotify.get_artist_id_from_name("My Chemical Romance", ["The Black Parade"]))))

rym.exit_browser()