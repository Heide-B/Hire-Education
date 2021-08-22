#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


df = pd.read_csv('df_with_topics.csv')
df


# In[ ]:


alt.Chart(df).mark_bar().encode(
    x='title', y='Dominant_Topic'
)


# In[ ]:


df['Dominant_Topic'].hist()


# In[ ]:


top20jobs = df['title'][:20]


# In[ ]:


test = df.groupby(df['title']).sum().sort_values(ascending=False, by='Document_No')


# In[ ]:


test[:10]


# In[ ]:


test['Unnamed: 0'].hist()


# In[ ]:


b = df.groupby(['Dominant_Topic', 'company']).sum()
b.reset_index(inplace=True)


# In[ ]:


t1 = b[b['Dominant_Topic'] == 0.0].sort_values(ascending=False, by='Unnamed: 0')[:5]


# In[ ]:


t2 = b[b['Dominant_Topic'] == 1.0][:5].sort_values(ascending=False, by='Unnamed: 0')[:5]


# In[ ]:


t3 = b[b['Dominant_Topic'] == 2.0][:5].sort_values(ascending=False, by='Unnamed: 0')[:5]


# In[ ]:


t4 = b[b['Dominant_Topic'] == 3.0].sort_values(ascending=False, by='Unnamed: 0')[:5]


# In[ ]:


alt.Chart(t4).mark_bar().encode(
y='company', x='Unnamed: 0'
)


# In[ ]:




