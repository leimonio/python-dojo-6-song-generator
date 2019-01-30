from __future__ import print_function
import requests
import random

artists_to_songs =	{
  "David Bowie": "Heroes",
  "Coldplay": "Yellow",
  "Cranberries": "Linger",
  "Nena": "99 Red Balloons",
  "Psy": "Gangnam style",
  "Netta": "toy"
}

BASE_API_URL = "https://api.lyrics.ovh/v1/"

def get_lyrics():
    lyrics_list = []
    for artist in artists_to_songs:
        song_url = BASE_API_URL + artist + "/" + artists_to_songs[artist]
        response = requests.get(song_url)
        response_json = response.json()
        lyrics_list.append(response_json["lyrics"])
    return lyrics_list

def extract_lyrics_lines(lyrics_list):
    all_lyrics_list = []
    for lyrics in lyrics_list:
        all_lyrics_list = all_lyrics_list + [line for line in lyrics.split('\n') if line]
    return all_lyrics_list

def main():
    lyrics_list = get_lyrics()
    all_lyrics_lines = extract_lyrics_lines(lyrics_list)
    random.shuffle(all_lyrics_lines)

    for i in range(20):
        index = random.randint(1,len(all_lyrics_lines))
        print(all_lyrics_lines[index])
        if i % 5 == 0:
            print('\n', end='')

if __name__== "__main__":
  main()
