import pandas as pd

lyrics = pd.read_csv('cleanedLyricsSmall.csv')

lyrics = lyrics[['song','artist','genre','splitLyrics']]
lyrics = lyrics.drop(601)
#%%
from langdetect import detect

top200 = lyrics.artist.value_counts()[:150]
smaller = [top200.index[i] for i in range(150)]
test = lyrics[lyrics.artist.isin(smaller)]

#def isEnglish(s):
#    try:
#        s.encode(encoding='utf-8').decode('ascii')
#    except UnicodeDecodeError:
#        return False
#    else:
#        return True

indices = []
corrected = []
for index, row in test.iterrows():
    if (detect(row.splitLyrics) == 'en') & (row.splitLyrics[0] == "["):
#        print(index, row.song) 
        indices.append(index)
        corrected.append(eval(row.splitLyrics))
print(len(corrected))

smaller = lyrics.iloc[indices]
smaller.splitLyrics = corrected
smaller = smaller.reset_index()

#%%
import numpy as np
import gensim
from gensim.test.utils import get_tmpfile

dictionary = gensim.corpora.Dictionary(smaller.splitLyrics)
corpus = [dictionary.doc2bow(lyric) for lyric in smaller.splitLyrics]

tf_idf = gensim.models.TfidfModel(corpus)

index_temp = get_tmpfile("index")
sims = gensim.similarities.Similarity("sims.txt", tf_idf[corpus],
                                      num_features=len(dictionary))

dictionary.save("dict.txt")
tf_idf.save("tfidf.txt")
sims.save("sims.txt")
