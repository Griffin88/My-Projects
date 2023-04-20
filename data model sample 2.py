import numpy as np
import pandas as pd

ratings = pd.read_csv(r'C:\Users\Griffin\Downloads\a\rating.csv', delimiter=',', nrows = 50000)
anime = pd.read_csv(r'C:\Users\Griffin\Downloads\a\anime.csv')

anime.head()

ratings.head()

anime.drop(anime.columns[3:], axis=1, inplace=True)

anime.dropna()
ratings.dropna(axis = 1, inplace = True)

def replace_name(x): 
    return anime[anime['anime_id']==x].name.values[0]

ratings.anime_id = ratings.anime_id.map(replace_name)

M = ratings.pivot_table(index=['user_id'],columns=['anime_id'],values='rating')

M.shape

def pearson(s1, s2): 
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c **2)) 

pearson(M['Naruto'], M['Tengen Toppa Gurren Lagann'])

pearson(M['Sekirei'], M['Tokyo Ghoul'])

pearson(M['Sword Art Online'], M['Sword Art Online II'])

ratings.to_csv(r'C:\Users\Griffin\Downloads\a\final.csv')