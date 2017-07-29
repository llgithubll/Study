# coding:utf8
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import jieba
import pprint
import os
from word_segmentation import *
import numpy as np
from PIL import Image


file_path = os.getcwd() + '\\'


def gen_word_cloud_base_cut(file_name):
    with open(file_path + file_name, 'r', encoding='utf-8') as f:
        word_cloud = WordCloud().generate(f.read())
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()


def gen_word_cloud_base_ori_freq(file_name):
    word_cloud = WordCloud().fit_words(get_word_freq(file_name))
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()



def gen_word_cloud_base_cut_use_mark(file_name, img):
    img_mark = np.array(Image.open(file_path + img))
    wc = WordCloud(background_color='white', max_words=61, \
                    mask=img_mark, stopwords=STOPWORDS.add('amp'))
   
    with open(file_path + file_name, 'r', encoding='utf-8') as f:
        wc.generate(f.read())
        plt.imshow(wc)
        plt.axis('off')
        plt.show()



if __name__ == '__main__':
    gen_word_cloud_base_cut('安大_cut')
    gen_word_cloud_base_ori_freq('安大')
    gen_word_cloud_base_cut_use_mark('安大_cut', 'black_and_white.jpg')