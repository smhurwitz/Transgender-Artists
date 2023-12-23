import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class RYM():
    def __init__(self):
        self.browser = Browser()

    def exit_browser(self):
        self.browser.close()
        self.browser.quit()

    """ Returns a dictionary containing information on the artist with the RYM profile url provided. """
    def artist_info(self, url="https://rateyourmusic.com/artist/my-chemical-romance"):
        def get_current_location(soup):
            if('Currently</div><div class="info_content' in str(soup)):
                s = str(soup).split('Currently</div><div class="info_content">')[1].split('</div><div')[0]
                if '">' in s: return s.split('">')[1].split('</a>')[0]
                else: return s
            return ''
        
        def get_followers(soup):
            return str(soup).split('<span class="label_num_followers">')[1].split(' followers')[0].replace(',','')
            
        def get_genres(soup):
            genres_soup = soup.find_all("a", {"class": "genre"})
            if genres_soup == None: return
            return [genre_soup.string for genre_soup in genres_soup]
        
        def get_name(soup):
            return str(soup.find("h1", {"class": "artist_name_hdr"})).split('<h1 class="artist_name_hdr">')[1].split('<')[0].strip().replace('&amp;', '&')

        def get_soup():
            self.browser.get_url(url)
            return self.browser.get_soup()
        
        def get_works(soup):
            works = []
            sections = str(soup).split('<h3 class="disco_header_label">') # RYM sections, e.g. Album or EP
            for section in sections:  # for each section...
                section_soup = BeautifulSoup(section, "lxml")

                format_dirty = section_soup.find("html").find("body").find("p")  
                if format_dirty == None: format = ''
                else: format = str(format_dirty).split('<p>')[1].split('</p>')[0].split('\n')[0]

                allowed_formats = ['Album', 'EP', 'Single', 'Live Album']
                if any([format == f for f in allowed_formats]):
                    nums_ratings = section_soup.find_all("div", {"class": "disco_ratings"})  
                    infos        = section_soup.find_all("div", {"class": "disco_info"})
                    ratings      = section_soup.find_all("div", {"class": "disco_avg_rating"})
                    for i in range(len(nums_ratings)):
                        work={}
                        title = str(infos[i].find("a")).split('title=')[1]
                        work['title']       = title.split('"')[1].split('"')[0] if title[0] == '"' else title.split('\'')[1].split('\'')[0]
                        work['num ratings'] = float(nums_ratings[i].string.replace(',','')) if not nums_ratings[i].string == None else 0
                        work['rating']      = float(ratings[i].string) if not ratings[i].string == None else 0
                        work['format']      = format
                        works.append(work)
            
            return works

        if not 'rateyourmusic.com/artist/' in url: 
            raise ValueError('The url provided must link to a RYM artist profile.')
        soup = get_soup()
        return {
            'name':             get_name(soup),
            'followers':        get_followers(soup),
            'genres':           get_genres(soup),
            'works':            get_works(soup),
            'current location': get_current_location(soup)
        }

    """ Returns an array of artist RYM url profiles from RYM list pages. """
    def artists_from_lists(self, list_urls=["https://rateyourmusic.com/list/limbs/trans-musicians/"]):
        urls=[]
        for list_url in list_urls:
            page_no = 1
            while(page_no == 1 or len(tags)>0):
                self.browser.get_url(list_url+str(page_no)+"/")
                soup = self.browser.get_soup()
                tags=soup.find_all("a", {"class": "list_artist"})
                for tag in tags:
                    url = "https://rateyourmusic.com/artist" + str(tag).split('/artist')[1].split('"')[0]
                    if (not "various-artists" in url) and (not url in urls): urls.append(url)
                page_no+=1
        urls.sort()
        return urls


"""This class is adapted from https://github.com/dbeley/rymscraper"""
class Browser(webdriver.Firefox):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Starting Selenium Browser : headless = %s")
        self.options = Options()
        self.options.add_argument('-headless')
        webdriver.Firefox.__init__(self, options=self.options)

    def restart(self):
        self.quit()
        webdriver.Firefox.__init__(self, options=self.options)

    def get_url(self, url):
        self.logger.debug("get_url(browser, %s)", url)
        while True:
            self.get(str(url))
            class_to_click_on = [
                "as-oil__btn-optin",  # cookie bar
                "fc-cta-consent",  # consent popup
                # "ad-close-button",  # advertisement banner
            ]
            for i in class_to_click_on:
                if len(self.find_elements(By.CLASS_NAME, i)) > 0:
                    self.find_element(By.CLASS_NAME, i).click()
                    self.logger.debug(f"{i} found. Clicking on it.")

            if len(self.find_elements(By.CLASS_NAME, "disco_expand_section_link")) > 0:
                try:
                    for index, link in enumerate(
                        self.find_elements(By.CLASS_NAME, "disco_expand_section_link")
                    ):
                        self.execute_script(
                            f"document.getElementsByClassName('disco_expand_section_link')[{index}].scrollIntoView(true);"
                        )
                        link.click()
                        time.sleep(0.2)
                except Exception as e:
                    self.logger.debug('No "Show all" links found : %s.', e)
            # Test if IP is banned.
            if self.is_ip_banned():
                self.quit()
                raise Exception("IP banned from rym. Can't do any requests to the website. Exiting.")
            # Test if browser is rate-limited.
            if self.is_rate_limited():
                self.logger.error("Rate-limit detected. Restarting browser.")
                self.restart()
            else:
                break
        return

    def get_soup(self):
        return BeautifulSoup(self.page_source, "lxml")

    def is_ip_banned(self):
        self.logger.debug("soup.title : %s", self.get_soup().title)
        return self.get_soup().title.text.strip() == "IP blocked"

    def is_rate_limited(self):
        return self.get_soup().find("form", {"id": "sec_verify"})