# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 17:14:05 2016

@author: Rapssail
"""

from Meetup import load_meetup_members
import numpy as np
import pandas as pd
from collections import Counter

members_data = load_meetup_members()
df = pd.DataFrame(members_data)
df.head()

def clean_df(df):
    cleaned_df = df[df.astype(unicode)['topics'] != '[]']
    return cleaned_df

def return_interests(cleaned_df):
    interests_corpus = cleaned_df.iloc[:,4]
    return interests_corpus

def count_most_common_interests(interests_corpus):
    c = Counter()
    for e in interests_corpus:
        person_interests = []
        for i in e:
            person_interests.append(i['name'])
        c.update(person_interests)

    return c.most_common(10)


    
