from googlesearch import search
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
from pytube import YouTube
import os


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
    # rank = song.find("span", class_="chart-element__rank__number").text.strip()
    title = song.find("span",
                      class_="chart-element__information__song").text.strip()
    artist = song.find(
        "span", class_="chart-element__information__artist").text.strip()

    song_info = {
        "title": title,
        "artist": artist,
    }
    
    return song_info

def scrapeSummerSongs():
    # Scrape songs
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
    # rank = song.find("span", class_="chart-element__rank__number").text.strip()
    title = song.find("span",
                      class_="chart-list-item__title-text").text.strip()
    artist = song.find(
        "div", class_="chart-list-item__artist").text.strip()

    song_info = {
        "title": title,
        "artist": artist,
    }
    
    return song_info


def scrapeTopYouTubeVideo(user_input):
    search_keyword = user_input.replace(" ", "+")
    youtube_url = 'https://www.youtube.com/results?search_query=' + search_keyword
    html = urllib.request.urlopen(youtube_url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    
    return "https://www.youtube.com/watch?v=" + video_ids[0]

def downloadYouTubeVideoFromURL(youtube_url, destination_path='./downloads'):
    yt = YouTube(youtube_url)
    
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    # download the file
    out_file = video.download(output_path=destination_path)

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    # result of success
    print(yt.title + " has been successfully downloaded.")
    
def downloadYouTubeVideoWithUserInput():
    user_input = str(input('Enter YouTube video to scrape then download:\n>>'))
    video_url = scrapeTopYouTubeVideo(user_input)
    downloadYouTubeVideoFromURL(video_url)