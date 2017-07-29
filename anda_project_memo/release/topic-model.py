
# coding: utf-8

# In[1]:


import pandas as pd
df = pd.read_csv("datascience.csv", encoding='gb18030')


# In[2]:


df.head()


# In[3]:


df.shape


# In[4]:


import jieba


# In[7]:


def chinese_word_cut(mytext):
    return ' '.join(jieba.cut(mytext))


# In[8]:


df["content_cutted"] = df.content.apply(chinese_word_cut)


# In[9]:


df.content_cutted.head()


# In[11]:


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


# In[12]:


n_features = 1000
tf_vectorizer = CountVectorizer(strip_accents = 'unicode', max_features=n_features, stop_words='english',max_df = 0.5,min_df = 10)
tf = tf_vectorizer.fit_transform(df.content_cutted)


# In[13]:


from sklearn.decomposition import LatentDirichletAllocation


# In[14]:


n_topics = 5
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50, learning_method='online', learning_offset=50, random_state=0)


# In[15]:


lda.fit(tf)


# In[16]:


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print('Topic #{}:'.format(str(topic_idx)))
        print(' '.join([feature_names[i] for i in topic.argsort()[:-n_top_words-1:-1]]))
        print()


# In[17]:


n_top_words = 20
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)


# In[20]:


import pyLDAvis
import pyLDAvis.sklearn
pyLDAvis.enable_notebook()
pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)


# In[ ]:




