# coding: utf-8
import pandas as pd
import jieba
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pprint



# df = pd.read_csv('datascience.csv', encoding='gb18030')
df = pd.read_csv('all_beida.csv')
# pprint.pprint(df.head())
# print(df.shape)



def chinese_word_cut(mytext):
    return ' '.join(jieba.cut(mytext))

df["answer_cutted"] = df.answer.apply(chinese_word_cut)
# pprint.pprint(df.answer_cutted.head())


stopwords = codecs.open('stopwords.txt', 'r', encoding='utf-8')
stopwords = [w.strip() for w in stopwords]

n_features = 100
tf_vectorizer = CountVectorizer(strip_accents = 'unicode', max_features=n_features, \
                                stop_words=stopwords,max_df = 0.5,min_df = 10)
tf = tf_vectorizer.fit_transform(df.answer_cutted)




n_topics = 5
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50, \
                learning_method='online', learning_offset=50, random_state=0)
lda.fit(tf)




def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print('Topic #{}:'.format(str(topic_idx)))
        print(' '.join([feature_names[i] for i in topic.argsort()[:-n_top_words-1:-1]]))
        print()


n_top_words = 10
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)
