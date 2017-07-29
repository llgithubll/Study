import os
import jieba
import jieba.analyse
import pprint


file_path = os.getcwd() + '\\'


def cut_file(file_name):
    out_file = open(file_path + file_name + '_cut', 'w', encoding='utf-8')
    with open(file_path + file_name, 'r', encoding='utf-8') as f:
        sentences = f.readlines()
        for sentence in sentences:
            tags = jieba.cut(sentence.strip())
            print(' '.join(tags), file=out_file)
    out_file.close()


def get_word_freq(file_name, top_k=20):
    with open(file_path + file_name, 'r', encoding='utf-8') as f:
        text = f.read()
        tags = jieba.analyse.extract_tags(text, withWeight=True, topK=top_k)
        tags_dict = dict(tags)
        return tags_dict


if __name__ == '__main__':
    urls = {}
    urls_file_path = os.getcwd() + '\\' + 'urls'
    with open(urls_file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().split(',')
            urls[line[0]] = line[1]

    for keyword, url in urls.items():
        cut_file(keyword)
        # get_word_freq(keyword)
        print(keyword)