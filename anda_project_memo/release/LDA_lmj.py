import codecs
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim import corpora
from pprint import pprint


train = []

# stopwords.txt 网上下载
stopwords = codecs.open('stopwords.txt','r',encoding='utf8').readlines()
stopwords = [ w.strip() for w in stopwords ]

fp = codecs.open('安徽大学_cut','r',encoding='utf8')
for line in fp:
    line = line.split()
    train.append([ w for w in line if w not in stopwords ])

dictionary = corpora.Dictionary(train)
corpus = [ dictionary.doc2bow(text) for text in train ]
lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=100)

# 打印前20个topic的词分布
for i in lda.print_topics(20):
    print(i, end='\n\n')
