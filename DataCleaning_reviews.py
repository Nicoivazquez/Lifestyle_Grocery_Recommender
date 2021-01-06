import os
import json
import gzip
import pandas as pd

### load the meta data

data = []
def data_clean(meta_gz):
    with gzip.open(meta_gz) as f:
        for l in f:
            data.append(json.loads(l.strip()))

    # total length of list, this number equals total number of products
    print(len(data))

    # first row of the list
    print(data[0])

    # convert list into pandas dataframe

    df = pd.DataFrame.from_dict(data)

    print(len(df))

    df_reviews = df.drop(['reviewTime','unixReviewTime','image','style], axis=1) 
    #df_reviews = df[df['vote'].fillna('0')] # the fill na does not work yet. but I want it to be 0 for no votes
    df_reviews['helpful_votes'] = df_reviews['vote'] 
    df_reviews['rating'] = df_reviews['overall']
    df_reviews['reviewTitle'] = df_reviews['summary']
    df_reviews = df_reviews.drop(['overall','summary','vote'],axis=1)
    df_reviews = df_reviews.drop_duplicates(subset={"reviewerID","reviewerName","reviewText","reviewTitle"})
    return df_reviews

                          # how to save a csv
#imdb.to_csv('imdb_processed.csv', index=False)