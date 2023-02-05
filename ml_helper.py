from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import numpy as np
# import pandas as pd

def bag_of_words(data, is_print_feature_names=False, is_normalized=False, is_standard_scaler=True, delimiter='default'):
    # Choose Delimiter with Comma (,) or with word 
    vectorizer = CountVectorizer()
    if delimiter == 'comma':
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','))

    vectorized_X = vectorizer.fit_transform(data).todense()
    
    if is_print_feature_names:
        vectorizer.get_feature_names()
    
    if is_normalized:
        vectorized_X = normalization(vectorized_X,is_standard_scaler=is_standard_scaler)

    return np.asarray(vectorized_X), vectorizer.get_feature_names()

def normalization(data, is_standard_scaler=True):
    minmax_scaler = MinMaxScaler(feature_range=[0,1])
    standard_scaler = StandardScaler()

    vectorized_X = minmax_scaler.fit_transform(data)
    if is_standard_scaler:
        vectorized_X = standard_scaler.fit_transform(data)

    return vectorized_X

def find_all_distance(vectorized_X, is_normalized_data=False, is_standard_scaler=False):
    # Show Data is Being Progress Every ? Data
    SHOW_i_DATA_EVERY = 400
    SHOW_j_DATA_EVERY = 400

    # -1 to reverse minmax scale
    # 0 means the closest => need to have the largest minmax scale
    multiply = -1 if is_normalized_data else 1
    scaler = None
    if is_normalized_data:
        scaler = MinMaxScaler(feature_range=[0,1])
        if is_standard_scaler:
            scaler = StandardScaler()
            
    memo_dist = {}
    lists_of_distances = []
    for i in range(len(vectorized_X)):
        distances = []
        for j in range(len(vectorized_X)):
            if i % SHOW_i_DATA_EVERY == 0 and j % SHOW_j_DATA_EVERY == 0:
                print('====================================')
                print(f'{i} => {j}')
                print('====================================')
            
            # I J Variable to str to ease maintenance
            ij, ji = str(i) + str(j), str(j) + str(i)
            
            if i == j:
                distances.append(0)
            elif ij in memo_dist:
                distances.append(memo_dist[ij])
            else:
                dist = euclidean_distances([vectorized_X[i]],[vectorized_X[j]])
                dist = dist[0][0] * multiply
                memo_dist[ji] = dist
                distances.append(dist)
                
        lists_of_distances.append(distances)
    
    if is_normalized_data:
        lists_of_distances = scaler.fit_transform(lists_of_distances)

    return lists_of_distances