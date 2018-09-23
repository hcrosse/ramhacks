import lyricsgenius as genius
import re

with open('genius_token', 'r') as f:
    token = f.read().strip('\n')

api = genius.Genius(token)


def get_lyrics(title, *artist):
    if type(artist) is tuple:
        lyrics = api.search_song(title).lyrics
    else:
        lyrics = api.search_song(title, artist).lyrics
    lyrics = re.sub(r"\[.*]", '', lyrics)
    return lyrics

