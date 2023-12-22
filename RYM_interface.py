from bs4 import BeautifulSoup

import util
import web_browser

class RYM():
    def __init__(self):
        self.browser = web_browser.Browser()

    def exit_browser(self):
        self.browser.close()
        self.browser.quit()

    """ Returns a dictionary containing the artist 'name', an array of their 'genres', and an array of their 'works'. 
        Each 'work' contains the 'title', 'type', 'num_ratings', and 'rating'. """
    def get_RYM_artist_info(self, artist_url="https://rateyourmusic.com/artist/my-chemical-romance"):
        self.browser.get_url(artist_url)
        soup = self.browser.get_soup()

        genres = []
        genres_soup = soup.find_all("a", {"class": "genre"})
        if not genres_soup == None:
            for genre_soup in genres_soup:
                genres.append(genre_soup.string)

        artist_name = str(soup.find("h1", {"class": "artist_name_hdr"})).split('<h1 class="artist_name_hdr">')[1].split('<')[0].strip().replace('&amp;', '&')
        works = []; total_num_ratings = 0; max_rating = 0

        sections = str(soup).split('<h3 class="disco_header_label">') # RYM sections, e.g. Album or EP
        for section in sections:  # for each section...
            section_soup = BeautifulSoup(section, "lxml")
            section_title = section_soup.find("html").find("body").find("p")  # specific name, e.g. "Album" or "EP"
            if not section_title == None:
                section_title = str(section_title).split('<p>')[1].split('</p>')[0].split('\n')[0]
                if "Album" in section_title or "EP" in section_title or "Single" in section_title or "Mixtape" in section_title:
                    num_ratingss = section_soup.find_all("div", {"class": "disco_ratings"})  # array of num ratings for all entries
                    infos = section_soup.find_all("div", {"class": "disco_info"})  # array of additional infos containing album titles for all entries
                    ratings = section_soup.find_all("div", {"class": "disco_avg_rating"})  # array of rating values for all entries
                    for i in range(len(num_ratingss)):
                        work={}
                        work_title = str(infos[i].find("a")).split('title=')[1]
                        if work_title[0] == '"': work_title = work_title.split('"')[1].split('"')[0]
                        else: work_title = work_title.split('\'')[1].split('\'')[0]
                        work['title'] = work_title

                        num_ratings = num_ratingss[i].string
                        if not num_ratings == None:
                            num_ratings = int(num_ratings.replace(',', ''))
                        work['num ratings'] = num_ratings

                        rating = ratings[i].string
                        if not rating == None:
                            rating = float(ratings[i].string)
                        work['rating'] = rating
                        work['type'] = section_title

                        works.append(work)

        mean_rating_num = 0;
        mean_rating_denom = 0;
        for work in works:
            if (not work['num ratings'] == None): total_num_ratings += work['num ratings']
            if (not work['rating'] == None):
                if work['type'] == 'Album' or work['type'] == 'EP' or work['type'] == 'Mixtape': max_rating = max(max_rating, work['rating'])
                mean_rating_num += work['num ratings'] * work['rating']
                mean_rating_denom += work['num ratings']
        if mean_rating_denom > 0: mean_rating = mean_rating_num / mean_rating_denom
        else: mean_rating = None
        if max_rating == 0: max_rating = None
        return {
            'name': artist_name,
            'genres': genres,
            'url': artist_url,
            'works': works,
            'mean rating': mean_rating,
            'max rating': max_rating,
            'number of ratings': total_num_ratings
        }

    """ Returns a url list of artists from a RYM List page. Prints to .txt file if print_list==True.
        Example url: https://rateyourmusic.com/list/limbs/trans-musicians/"""
    def get_artists_from_list(self, write_list=False, list_urls=["https://rateyourmusic.com/list/limbs/trans-musicians/"]):
        artist_urls=[]
        for list_url in list_urls:
            tags=[]
            page_no = 1
            while(page_no == 1 or len(tags)>0): #iterate over all pages over the list until no more entries
                self.browser.get_url(list_url+str(page_no)+"/")
                soup = self.browser.get_soup()
                tags=soup.find_all("a", {"class": "list_artist"})
                for tag in tags:
                    artist_url=str(tag).split('/artist')[1].split('"')[0] #returns e.g., /glass-beach
                    artist_url = "https://rateyourmusic.com/artist" + artist_url
                    if (not "various-artists" in artist_url) and (not artist_url in artist_urls): artist_urls.append(artist_url)
                page_no+=1
        artist_urls.sort()

        if write_list:
            file = open('artist_urls_from_lists.txt', 'w')
            for a in artist_urls: file.write(a+'\n')
            file.close()

        return artist_urls

    """ Returns array of names of all the works listed on Spotify. """
    def get_work_titles(self, artist_info):
        titles=[]
        works = artist_info['works']
        for work in works:
            titles.append(work['title'])
        return titles

    """ Nicely prints the artist's info to screen. Takes the output of 'get_RYM_artist_info'. """
    def print_artist_info(self, artist_info):
        print("Name: " + artist_info['name'])
        print("Genres: " + util.array_to_string(artist_info['genres']))
        print("Number of ratings: " + str(round(artist_info['number of ratings'],2)))
        print("Mean rating: " + str(artist_info['mean rating']))
        print("Max rating: " + str(artist_info['max rating']))
        works = artist_info['works']
        for work in works:
            print(work)