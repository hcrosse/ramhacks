import re
import gensim
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stopwords = stopwords.words('english')
stopwords.extend(['im', 'id', 'thats', 'youre', 'aint', 'oh', ''])

songs = pd.read_csv("data/songs.csv")
songs.splitLyrics = [eval(lyric) for lyric in songs.splitLyrics]

dicty = gensim.corpora.Dictionary.load("data/dict.txt")
tfidf = gensim.models.TfidfModel.load("data/tfidf.txt")
sims = gensim.similarities.Similarity.load("data/sims.txt")


def recommend(query):
    query = query.replace('\n', ' ').lower().split()
    query = [re.sub(r'[^a-zA-Z]', "", q) for q in query]
    query = [q for q in query if q not in stopwords]

    query_bow = dicty.doc2bow(query)
    query_tfidf = tfidf[query_bow]

    result = sims[query_tfidf]

    top_5_indices = np.argpartition(result, -5)[-5:]
    top_5_indices = top_5_indices[np.argsort(result[top_5_indices])]
    max_values = result[top_5_indices]
    top_songs = songs.iloc[top_5_indices]
    titles = top_songs.song.str.title()
    artists = top_songs.artist.str.title()
    lyrics = [" ".join(lyric[:20]) for lyric in top_songs.splitLyrics]

    commonSongs = []
    for i in range(5):
        songInfo = {}
        songInfo['title'] = titles.iloc[i]
        songInfo['artist'] = artists.iloc[i]
        songInfo['lyrics'] = lyrics[i]
        commonSongs.append(songInfo)
    return commonSongs
