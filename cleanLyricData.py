import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
stopwords.extend(['im','id','thats','youre','aint','oh', ''])

lyrics = pd.read_csv('lyrics.csv')

#%%
lyrics = lyrics.drop('index', axis=1)
lyrics = lyrics.dropna(axis=0, subset=['lyrics'])

lyrics.song = lyrics.song.str.replace('-',' ')
lyrics.artist = lyrics.artist.str.replace('-',' ')

lyrics.lyrics = lyrics.lyrics.str.replace('\n',' ')
lyrics.lyrics = lyrics.lyrics.str.lower()

#%%
from nltk.stem.wordnet import WordNetLemmatizer    
from nltk.corpus import wordnet as wn

def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']
def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']

def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return wn.NOUN

#%%
splitLyrics = []
lemmatizer = WordNetLemmatizer()
for index, lyric in lyrics.iterrows():
    print(lyric.song)
    lyric = lyric.lyrics
    lyricList = [re.sub(r'[^a-zA-Z]', "", str) for str in lyric.split()]
    lyricList = [str for str in lyricList if str not in stopwords]
    tags = nltk.pos_tag(lyricList)
    lemms = [lemmatizer.lemmatize(tag[0],penn_to_wn(tag[1])) for tag in tags]
    splitLyrics.append(lemms)
    
lyrics['splitLyrics'] = splitLyrics
lyrics.to_csv('cleanedLyrics.csv')
