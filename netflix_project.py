# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 11:47:01 2023

@author: Saurabh
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 10:25:28 2023

@author: Saurabh
"""

import pandas as pd
import numpy as np

### cleaning data
file = r"C:\Users\Saurabh\Desktop\dsp\netflix_titles.csv"

df = pd.read_csv(file)

df.info()

## replacing or dropping missing values
df['country'] = df['country'].replace(np.nan,'Missing')
df['director'].fillna('Unknown',inplace = True)
df = df.loc[df["rating"].isna() == False]
df['cast'].fillna('Unknown',inplace = True)
df = df.loc[df["date_added"].isna() == False]



df['country'].nunique()

country_count = pd.DataFrame(df['country'].value_counts())
country_count.reset_index(inplace = True)
country_count.columns = ['country','count']
country_count = country_count[country_count['count'] > 8]

## genre
genre = pd.DataFrame(df['listed_in'].value_counts())
genre.reset_index(inplace = True)
genre.columns = ['listed_in','count']
genre = genre[genre['count'] > 46]



## dropped for countries where frequency is less than 9
df = df[df.country.isin(country_count['country'])]
df = df[df.listed_in.isin(genre['listed_in'])]

df.columns

df['date_added'] = pd.to_datetime(df['date_added'])

 
### rating
df.rating.unique()
r = pd.DataFrame(df.rating.value_counts())

r.index
## don't need ratings below this frequency
r = r[r.rating >= 33]
df = df[df.rating.isin(r.index)]


r.reset_index(inplace = True)
r.columns = ['rating','count']

## to understand it better 
ratings_ages = {
    'PG-13': 'Teens',
    'TV-MA': 'Adults',
    'PG': 'Pre Teen',
    'TV-14': 'Teens',
    'TV-PG': 'Adults',
    'TV-Y':'Kids',
    'TV-Y7': 'Pre Teen',
    'R': 'Adults',
    'TV-G': 'Kids',
    'G': 'Kids',
    'NR': 'Adults'
}

df['target_age'] = df['rating']
df['target_age'] = df['rating'].replace(ratings_ages)

## will drop missing row
## get graph of country wise content distribution

top_c = country_count[:7]
top_c.drop(2,inplace = True)
top_c.reset_index(inplace = True)
top_c = top_c.drop(['index'],axis = 'columns')

genre_target_tv = pd.DataFrame(df_tv.groupby(['target_age','listed_in'])['show_id'].count())
genre_target_tv.reset_index(inplace = True)
genre_target_tv.rename(columns = {'show_id':'count'}, inplace = True)


piv = pd.pivot_table(genre_target_tv, values="count",index=["target_age"], columns=["listed_in"], fill_value=0)




#### might need later but this is for general info ki kya karna hain 

df_movies = df[df.type == 'Movie']
df_tv = df[df.type == 'TV Show']

## general
r_age = pd.DataFrame(df.groupby(['rating','target_age'])['show_id'].count())
r_age.reset_index(inplace = True)
r_age.rename(columns = {'show_id':'count'}, inplace = True)


## for tv
r_age_tv = pd.DataFrame(df_tv.groupby(['rating','target_age'])['show_id'].count())
r_age_tv.reset_index(inplace = True)
r_age_tv.rename(columns = {'show_id':'count'}, inplace = True)

## for movies
r_age_movie = pd.DataFrame(df_movies.groupby(['rating','target_age'])['show_id'].count())
r_age_movie.reset_index(inplace = True)
r_age_movie.rename(columns = {'show_id':'count'}, inplace = True)

duration = pd.DataFrame(df_tv['duration'].value_counts().nlargest(5))
duration = duration.reset_index()
duration.columns = ['duration','count']














#### some plots
import matplotlib.pyplot as plt
##plt.pie(df['type'].value_counts(),label = df['type'].unique(),autopct='%1.1f%%')

b = df['type'].value_counts().reset_index()
b.columns = ['type','count']

### plot to see distribution of tv and movies
plt.pie(b['count'],labels= b.type,autopct='%1.1f%%')


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(15,8))
sns.barplot(x = 'country',y = 'count',data = top_c).set(title = 'Amount of content by country')

### see how recent or old the content in general is
sns.histplot(data=df, x="release_year",bins= 50,hue = 'type')


plt.figure(figsize = [10,8])
sns.pointplot(x = "rating",
              y = "count",
              data = r)

sns.barplot(data = r_age,x = "target_age", y="count",ci = None).set(title = 'General Content Made For Age Groups')
sns.barplot(data = r_age_tv,x = "target_age", y="count",ci =None).set(title = 'Age Distribution on TV Shows')
sns.barplot(data = r_age_movie,x = "target_age", y="count",ci = None).set(title = 'Age Distribution on Movies on Netflix')





## to see what's the duration on tv usually
plt.figure(figsize = [10,8])
sns.barplot(data=duration, x="duration",y='count').set(title = 'Usual Duration of  A TV Series')



### how it is targeted 
sns.heatmap(piv, square=True).set(title = 'Targeted Audience for Genre')
    





