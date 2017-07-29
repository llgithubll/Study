# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os
import pprint
import re
from bs4 import BeautifulSoup


def union_file(input_files, out_file):
    all_lines = set()
    for file in input_files:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[1:] # not count title
            for line in lines:
                all_lines.add(line)

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('question,answer\n')
        for line in all_lines:
            f.write(line) 


class ZhiHu():
    def __init__(self):
        self.file_path = os.getcwd() + '\\'
        self.driver = webdriver.Firefox()    

    def access(self, keyword, url):
        cookie = self.driver.get_cookies()
        time.sleep(2)
        
        self.driver.get(url)
        time.sleep(3)

        print('Get from: ' + url)
        print('About: ' + keyword)
        
        cnt = 1
        ceil_cnt = 10
        while True:
            try:
                self.driver.find_element_by_css_selector('.zg-btn-white.zu-button-more').click()
                time.sleep(2)
                print('click:' + str(cnt))
                cnt += 1
                # if cnt > ceil_cnt: # avoid at this while too long or something wrong
                #     break
            except:
                break
    
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        with open(keyword + '.csv', 'w', encoding='utf-8') as f:
            f.write('question,answer\n')
            idx = 0
            for item in soup.find_all('li', {'class':'item clearfix', 'data-type':'Answer'}):
                # f.write(str(idx) + ',\t' + str(item) + '\n')
                ques = item.find('a', {'class':'js-title-link', 'target':'_blank'})
                author = item.find('a', {'class':'author author-link'})
                answer = item.find('script', {'type':'text', 'class':'content'})
                votes = item.find('span', {'class':'count'})

                # print(str(idx) + 'ques:' + '\t' + ques.get_text())
                # print(str(idx) + 'votes:' + '\t' + votes.get_text())
                # print(str(idx) + 'author:' + '\t' + ('匿名用户' if author is None else author.get_text()))
                # print(str(idx) + 'answer:' + '\t' + answer.get_text())

                # 每个问答一行，要消除问与答中的换行
                # 因为要用英文的逗号,作为csv文件的分隔符，所以对于问题或答案中的英文,转成中文逗号，避免对csv文件造成影响
                # 将回答中的超链接换成空格，避免其对文本数据的影响
                answer_text = answer.get_text()
                pure_answer_text = re.sub(r'<.*?>', ' ', answer_text)
                pure_answer_text = re.sub(r',', '，', pure_answer_text)
                pure_answer_text = re.sub(r'\n', ' ', pure_answer_text)

                pure_question_text = re.sub(r',', '，', ques.get_text())
                pure_question_text = re.sub(r'\n', ' ', pure_question_text)
                
                # f.write('index:' + str(idx) + ',' \
                #         + 'question:' + ques.get_text() + ',' \
                #         + 'author:' + ('匿名用户' if author is None else author.get_text()) + ',' \
                #         + 'answer:' + pure_answer_text + ',' \
                #         + 'votes:' + votes.get_text() + '\n') 

                f.write(pure_question_text + ',' + pure_answer_text + '\n')
                idx += 1
        
        print(keyword, 'complete.', 'total {0} line datas'.format(str(idx)))

        

if __name__ == '__main__':
    zh = ZhiHu()

    urls = {}
    file_path = os.getcwd() + '\\' + 'urls'
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().split(',')
            urls[line[0]] = line[1]


    input_files = []
    for keyword, url in urls.items():
        zh.access(keyword, url)
        input_files.append(keyword + '.csv')
        time.sleep(3)

    union_file(input_files, 'all_beida.csv')



# 安大,https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%A4%A7
# 安徽大学,https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6
# 合工大,https://www.zhihu.com/search?type=content&q=%E5%90%88%E5%B7%A5%E5%A4%A7
# 合肥工业大学,https://www.zhihu.com/search?type=content&q=%E5%90%88%E8%82%A5%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6
# 中科大,https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E7%A7%91%E5%A4%A7
# 中国科技大学,https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6
# 清华,https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E
# 清华大学,https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6
# 北大,https://www.zhihu.com/search?type=content&q=%E5%8C%97%E5%A4%A7
# 北京大学,https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6
# 复旦,https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6
# 复旦大学,https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6%E5%A4%A7%E5%AD%A6
# 上交,https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E4%BA%A4
# 上海交通大学,https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E6%B5%B7%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%A6
# 浙大,https://www.zhihu.com/search?type=content&q=%E6%B5%99%E5%A4%A7
# 浙江大学,https://www.zhihu.com/search?type=content&q=%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6
# 南大,https://www.zhihu.com/search?type=content&q=%E5%8D%97%E5%A4%A7
# 南京大学,https://www.zhihu.com/search?type=content&q=%E5%8D%97%E4%BA%AC%E5%A4%A7%E5%AD%A6


# '安大':'https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%A4%A7',
# '安徽大学':'https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6',
# '合工大':'https://www.zhihu.com/search?type=content&q=%E5%90%88%E5%B7%A5%E5%A4%A7',
# '合肥工业大学':'https://www.zhihu.com/search?type=content&q=%E5%90%88%E8%82%A5%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6',
# '中科大':'https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E7%A7%91%E5%A4%A7',
# '中国科技大学':'https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6',
# '清华':'https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E',
# '清华大学':'https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6',
# '北大':'https://www.zhihu.com/search?type=content&q=%E5%8C%97%E5%A4%A7',
# '北京大学':'https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6',
# '复旦':'https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6',
# '复旦大学':'https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6%E5%A4%A7%E5%AD%A6',
# '上交':'https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E4%BA%A4',
# '上海交通大学':'https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E6%B5%B7%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%A6',
# '浙大':'https://www.zhihu.com/search?type=content&q=%E6%B5%99%E5%A4%A7',
# '浙江大学':'https://www.zhihu.com/search?type=content&q=%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6',
# '南大':'https://www.zhihu.com/search?type=content&q=%E5%8D%97%E5%A4%A7',
# '南京大学':'https://www.zhihu.com/search?type=content&q=%E5%8D%97%E4%BA%AC%E5%A4%A7%E5%AD%A6'