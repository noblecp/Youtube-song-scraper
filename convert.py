file = open('songsFull.txt', 'r')
songs = file.readlines()
songs.sort()

open('/Users/noblecp/desktop/Youtube-song-scraper/song_list.txt', 'w').close()
toFile = open('/Users/noblecp/desktop/Youtube-song-scraper/song_list.txt', 'a')

open('/Users/noblecp/desktop/Youtube-song-scraper/songsFull.txt', 'w').close()
sortFile = open('/Users/noblecp/desktop/Youtube-song-scraper/songsFull.txt', 'a')

for song in songs:
    sortFile.write(song)
    if song == "\n":
        song = ""
    song = song.lower()
    song = song.replace("[", "")
    song = song.replace("]", "")
    song = song.replace("(", "")
    song = song.replace(")", "")
    song = song.replace("feat. ", "")
    song = song.replace("&", "")
    song = song.replace(".", "")
    song = song.replace("'", "")
    song = song.replace("/", "")
    song = song.replace("  ", " ")
    song = song.replace("ü", "u")
    song = song.replace("ë", "e")
    toFile.write(song)

toFile.close()
sortFile.close()