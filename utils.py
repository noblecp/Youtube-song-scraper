from googlesearch import search
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import subprocess
import os

# Constants
CURRENT_DIRECTORY = os.path.abspath("downloads")

# BILLBOARD HOT 100 ----------------------------------------------------------------
def scrapeBillboard():
    # Scrape songs
    billboard_url = "https://www.billboard.com/charts/hot-100"
    html = requests.get(billboard_url)
    soup = BeautifulSoup(html.text, "lxml")
    scraped_songs = soup.findAll("li", class_="chart-list__element")

    num_songs_to_scrape = int(
        input("Enter top # of songs to scrape then download(between 1 and 100)\n>> "))

    total_scraped = 0
    song_list = []
    for song in scraped_songs:
        song_info = getBillboardSongInfo(song)
        full_song_name = song_info['artist'] + " " + song_info['title']
        yt_video_url = scrapeTopYouTubeVideo(full_song_name)
        downloadYouTubeVideoFromURL(yt_video_url)
        
        total_scraped += 1
        if(total_scraped == num_songs_to_scrape):
            return

def getBillboardSongInfo(song):
    title = song.find("span",
                      class_="chart-element__information__song").text.strip()
    artist = song.find(
        "span", class_="chart-element__information__artist").text.strip()

    song_info = {
        "title": title,
        "artist": artist,
    }
    
    return song_info

# SUMMER SONGS ----------------------------------------------------------------
def scrapeSummerSongs():
    # Scrape songs from website
    sumer_songs_url = "https://www.billboard.com/charts/summer-songs"
    html = requests.get(sumer_songs_url)
    soup = BeautifulSoup(html.text, "lxml")
    scraped_songs = soup.findAll("div", class_="chart-list-item")

    num_songs_to_scrape = int(
        input("Enter top # of songs to scrape then download(between 1 and 20)\n>> "))

    total_scraped = 0
    song_list = []
    for song in scraped_songs:
        song_info = getSummerSongInfo(song)
        full_song_name = song_info['artist'] + " " + song_info['title']
        yt_video_url = scrapeTopYouTubeVideo(full_song_name)
        downloadYouTubeVideoFromURL(yt_video_url)
        
        total_scraped += 1
        if(total_scraped == num_songs_to_scrape):
            return

def getSummerSongInfo(song):
    # rank = song.find("DIV", class_="chart-list-item__rank ").text.strip()
    title = song.find("span",
                      class_="chart-list-item__title-text").text.strip()
    artist = song.find(
        "div", class_="chart-list-item__artist").text.strip()

    song_info = {
        "title": title,
        "artist": artist,
    }
    
    return song_info

# UTILS ------------------------------------------------------------------------------------
def downloadYouTubeVideoWithUserInput():
    user_input = str(input('Enter YouTube video name to scrape then download:\n>>'))
    video_url = scrapeTopYouTubeVideo(user_input)
    downloadYouTubeVideoFromURL(video_url, user_input)
    
def downloadYouTubeVideoWithString(string):
    video_url = scrapeTopYouTubeVideo(string)
    downloadYouTubeVideoFromURL(video_url, string)
    
def scrapeTopYouTubeVideo(user_input):
    try:
        search_keyword = user_input.replace(" ", "+")
        youtube_url = 'https://www.youtube.com/results?search_query=' + search_keyword
        html = urllib.request.urlopen(youtube_url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        
        print("Found YouTube video for: ", user_input)
        return "https://www.youtube.com/watch?v=" + video_ids[0]
    except:
        print("Failed to find video for: ", user_input);

def downloadYouTubeVideoFromURL(youtube_url, user_input):
    try:
        print("Downloading video..")
        file_name = user_input.replace(" ", "_").title() + ".mp4"
        download_path = os.path.join(CURRENT_DIRECTORY, file_name)
        print(download_path)
        command = "youtube-dl -o " + download_path + " --extract-audio --audio-format mp3 " + youtube_url
        download_code = subprocess.call(command, shell=True)  
        print("Download successful!")
    except: 
        print("Download failed.")
        
        
# FILE DOWNLOAD -------------------------------------------------------------------------
def downloadFromTextFile():
    print("Downloading songs from text file..")
    text_file = open('song_list.txt', 'r')
    songs = text_file.readlines()
    
    for song in songs:
        downloadYouTubeVideoWithString(song.strip())
    
# CHART SELECTION -----------------------------------------------------------------------------
def scrapeByChart():
    choices = {
        'Songs of the Summer':
        'scrapeSummerSongs()',
        'Billboard Hot Top 100':
        'scrapeBillboard()',
    }

    # Increment index by 1 to make it more user-friendly
    for index, (key, value) in enumerate(choices.items()):
        print(index + 1, ': ', key)

    choices_list = list(choices)
    user_choice = int(input('Enter a choice: '))

    eval(choices[choices_list[user_choice - 1]])