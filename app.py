from bs4 import BeautifulSoup
import requests
from googlesearch import search
import webbrowser

# ask user whether to open YouTube to MP3 downloader website or not
if input("Open online YouTube to mp3 (y/n)?\n>> ") == "y":
    webbrowser.open("https://ytmp3.cc/downloader/", 1)

# determine the functionality requested, either web scraping or individual search
functionality = int(input("1) web scrape top songs\n2) search by song title\n>> "))

# SCRAPE TOP SONGS
if functionality == 1:
    # ------------------ WEB SCRAPING SONGS ------------------
    # declare url and use requests module to query the page from the url
    url = "https://www.billboard.com/charts/hot-100"
    html_text = requests.get(url)

    # parse the html using BeautifulSoup
    soup = BeautifulSoup(html_text.text, "lxml")

    # get all songs on billboard page based on html tags
    songs = soup.findAll("li", class_="chart-list__element")

    # Request input from user for how many songs to scrape
    num_songs = int(input("Enter how many top songs to view (between 1 and 100)\n>> "))
    
    # store songs in array
    song_list = []

    # loop through each song and display relavent data per song
    for song in songs:
        # get rank
        rank = song.find("span", class_="chart-element__rank__number").text.strip()
        if int(rank) <= num_songs:
            # get title
            title = song.find("span", class_="chart-element__information__song").text.strip()
            # get artist
            artist = song.find("span", class_="chart-element__information__artist").text.strip()
            
            # append to list of songs
            song_list.append({
                "title": title,
                "artist": artist,
                "rank": rank,
            })

    # ------------------ GOOGLE SEARCHING ------------------
    option = int(input("1) Open all \n2) Print songs\n>> "))

    for song in song_list:
        song_title = song["title"]      # get song title
        song_artist = song["artist"]    # get song artist
        query = song_title + " by " + song["artist"]    # form google search query

        result = search(query, num_results=1)
        print(song_title, "by", song_artist)
        if option == 1:
            for i in result:
                webbrowser.open(i, 2)
        
        elif option == 2:
            for i in result:
                print ("<< " + i)

# SEARCH BY SONG
elif functionality == 2:
    query = input("Search song by title\n>> ")
    result = search(query, num_results=1)
    for i in result:
        if input("Open link in new tab (y/n)?\n>> ") == "y":
            webbrowser.open(i, 2)
        else:
            print ("<< " + i)
            
