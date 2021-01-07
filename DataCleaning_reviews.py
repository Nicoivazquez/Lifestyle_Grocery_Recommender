import os
import json
import gzip
import pandas as pd

import numpy as np
import pandas as pd

#preprocessing
import string 
import nltk
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from nltk.corpus import stopwords  #stopwords
from nltk import word_tokenize,sent_tokenize # tokenizing
from nltk.stem import PorterStemmer,LancasterStemmer  # using the Porter Stemmer and Lancaster Stemmer and others
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer  # lammatizer from WordNet
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


stemmer_porter=PorterStemmer()
s_words = set(stopwords.words('english'))
punc = set(string.punctuation)

### load the meta data

data = []
def data_clean(meta_gz):
    with gzip.open(meta_gz) as f:
        for l in f:
            data.append(json.loads(l.strip()))
    # first row of the list
    print(data[0])
    # convert list into pandas dataframe
    df = pd.DataFrame.from_dict(data)
    # Drop the rows I don't use in this model
    df_reviews = df.drop(['reviewTime','unixReviewTime','image','style'], axis=1) 
    #df_reviews = df[df['vote'].fillna('0')] # the fill na does not work yet. but I want it to be 0 for no votes
    df_reviews['helpful_votes'] = df_reviews['vote'] 
    df_reviews['rating'] = df_reviews['overall']
    df_reviews['reviewTitle'] = df_reviews['summary']
    df_reviews = df_reviews.drop(['overall','summary','vote'],axis=1)
    df_reviews = df_reviews.drop_duplicates(subset={"reviewerID","reviewerName","reviewText","reviewTitle"})
    return df_reviews



def all_text_processing(df):
    df["all_text"] = df["reviewText"] + df["reviewTitle"]
    df['cleanText1']= df['all_text'].apply(lambda words:" ".join([word for word in words.split() if word not in s_words]))
    df['cleanText2'] = df['cleanText1'].apply(lambda words:" ".join(["".join([c if c not in punc else " " for c in word]) for word in words.split()]))
    df['cleanText3'] = df['cleanText2'].apply(is_only_alpha)
    df['cleanText4'] = df['cleanText3'].apply(word_tokenize)
    df['cleanText5'] = df['cleanText4'].apply(lambda words: [word.lower() for word in words])
    df['cleanText6'] = df['cleanText5'].apply(stemmers)
    df['reviewProcessed'] = df['cleanText6'].apply(lambda words: " ".join(words))
    df = df.drop(['cleanText1','cleanText2','cleanText3','cleanText4','cleanText5','cleanText6'],axis=1)
    return df


# how to save a csv
#imdb.to_csv('imdb_processed.csv', index=False)






