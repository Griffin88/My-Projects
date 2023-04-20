import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from ast import literal_eval
import scipy.cluster.hierarchy as hcluster
data = pd.read_csv(r'C:\Users\Griffin\Downloads\anime.csv')

#media type to 1 for tv, 0 for movie



#ongoing false = 0, true = 1 
data[data['ongoing'] == 'TRUE']['ongoing'] = 1
data[data['ongoing'] == 'FALSE']['ongoing'] = 0
#fill 0s 
data['votes'].fillna(0, inplace=True)
data['myrate'].fillna(0, inplace=True)

#drop empty rows
data = data.dropna(subset = ['watched', 'rating', 'startYr'])

#creating dumby variables for genres
test = data.tags.apply(literal_eval)
mlb = MultiLabelBinarizer()
df1 = pd.DataFrame(mlb.fit_transform(test),columns=mlb.classes_, index=data.index)
#creating dumby variables for studios 
test_2 = data.studios.apply(literal_eval)
mlb = MultiLabelBinarizer()
df2 = pd.DataFrame(mlb.fit_transform(test_2),columns=mlb.classes_, index=data.index) 


#concat dfs 
df_f = pd.concat([df1, df2, data], axis=1)
#reset index
df_f = df_f.reset_index()
#filtering cluster
#df_f = df_f[df_f['myrate'] != 0]

#save title as array
title_list = np.array(df_f['title'])
title_list2 = np.array(df_f['rating'])


#drop columns
df_f = df_f.drop(columns = ['ongoing','title','tags','studios','description','duration', 'contentWarn','sznOfRelease','finishYr', 'eps','watching', 'wantWatch', 'index'])

df_f.loc[df_f['mediaType'] == 'TV', 'mediaType'] = 1
df_f.loc[df_f['mediaType'] == 'Movie', 'mediaType'] = 0
df_f.loc[df_f['mediaType'] == 'DVD Special', 'mediaType'] = -1
df_f.loc[df_f['mediaType'] == 'Music Video', 'mediaType'] = -1
df_f.loc[df_f['mediaType'] == 'Other', 'mediaType'] = -1
df_f.loc[df_f['mediaType'] == 'OVA', 'mediaType'] = -1
df_f.loc[df_f['mediaType'] == 'TV Special', 'mediaType'] = -1
df_f.loc[df_f['mediaType'] == 'Web', 'mediaType'] = -1
df_f.loc[df_f['mediaType'] == '', 'mediaType'] = -1
df_f = df_f[df_f['mediaType'] != -1]


#convert to numeric
df_f = df_f.apply(pd.to_numeric)
#normalizing data
for x in df_f.columns: 
    df_f[x] = df_f[x]/(df_f[x].max()-df_f[x].min())
df_f = df_f.dropna(axis =1, how ='all')

print(df_f.columns[df_f.isna().any()].tolist())
print(df_f)
df_f = df_f.reset_index()
thresh = 3000
clusters = hcluster.fclusterdata(df_f, thresh, criterion="maxclust")
print(len(clusters))
print(df_f.shape)
#finds the best cluster according to my rating
def find_cluster(df):
    list_index = {}
    for c in clusters: 
        list_index[c] = 0
    for index in df.index:
        cluster = clusters[index]
        list_index[cluster] += df.at[index, 'myrate']
    curr_max = -np.inf
    for k, v in list_index.items(): 
        if v > curr_max:
            curr_max = v
            max_key = k 
    return max_key
#prints amount of clusters
z = {}
for x in clusters: 
    z[x] = 0 
for y in clusters: 
    z[y] += 1 
print(len(z.items()))

#prints out list from best cluster
max_index = find_cluster(df=df_f)
cluster_index = []
count = 0
print(clusters)
print(max_index)
for x in clusters: 
    if x == max_index: 
        count += 1 
print(count)
for x in range(len(clusters) - 1):
    if clusters[x] == max_index: 
        cluster_index.append(x)
x = [] 
for index in cluster_index: 
    x.append(title_list[index])
print(x)
y = [] 
for index in cluster_index: 
    y.append(title_list2[index])
print(y)
import pylab as pl
x1 = [0,1,2,3,4,5]
xTicks = x
y1 = y
pl.xticks(x1, xTicks)
pl.xticks(range(6), xTicks, rotation=45) #writes strings with 45 degree angle
pl.plot(x1,y1,'*')
pl.show()
#print(type(clusters[0]))
#print(clusters)
#(df_f.iloc[662])



    




         