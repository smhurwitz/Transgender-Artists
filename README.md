This repository is designed to scrape RateYourMusic (RYM) and interact with Spotify's API in order to gather data on
transgender musicians. The interfaces for RYM and Spotify are given in 'RYM_interface.py' and 'spotify_interface.py',
respectively. Artist information is stored in an Artist class defined in 'artist.py'. The runner for the program
is defined in 'main.py'. 

The runner contains methods to (1) take a text file of RYM artist lists urls (which may include RYM artist urls and 
Spotify artist urls) extract the urls of all artists listed; and (2) extract data from a list of RYM/Spotify artist urls.
The text file of RYM artist lists is given in 'artist_lists.txt' and includes a number of RYM lists on transgender artists,
as well as individual artist profiles I know or that others have shared with me. The text file 'artist_urls.txt' is the
result of performing method (1) on 'artist_lists.txt'. The text file 'output.py' gives a succint summary of the information
gathered from the internet.