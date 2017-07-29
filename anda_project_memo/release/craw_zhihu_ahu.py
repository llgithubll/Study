# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os
import pprint
import re
from bs4 import BeautifulSoup


class ZhiHu():
    def __init__(self):
        self.file_path = os.getcwd() + '\\'
        self.driver = webdriver.Firefox()

    def login(self):
        self.driver.get('https://www.zhihu.com')
        time.sleep(2)
        
        self.driver.find_element_by_link_text('登录').click()
        time.sleep(2)
        
        self.driver.find_element_by_name('account').send_keys('17352925828')
        time.sleep(2)

        self.driver.find_element_by_name('password').send_keys('lilin10000')
        time.sleep(2)

        wait = input('完成验证（选择倒立的字），控制台回车继续')
        self.driver.find_element_by_css_selector('div.button-wrapper.command > button').click()
        time.sleep(5)

        print('login success')
    

    def access(self, keyword, url):
        cookie = self.driver.get_cookies()
        time.sleep(2)
        
        self.driver.get(url)
        time.sleep(5)

        print('Get from: ' + url)
        print('About: ' + keyword)
        
        cnt = 1
        ceil_cnt = 10
        while True:
            try:
                self.driver.find_element_by_css_selector('.zg-btn-white.zu-button-more').click()
                time.sleep(4)
                print('click:' + str(cnt))
                cnt += 1
                if cnt > ceil_cnt: # avoid at this while too long or something wrong
                    break
            except:
                break
    
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        with open(keyword, 'w', encoding='utf-8') as f:

            idx = 1
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

                answer_text = answer.get_text()
                pure_answer_text = re.sub(r'<.*?>', ' ', answer_text)
                # f.write('index:' + str(idx) + ',' \
                #         + 'question:' + ques.get_text() + ',' \
                #         + 'author:' + ('匿名用户' if author is None else author.get_text()) + ',' \
                #         + 'answer:' + pure_answer_text + ',' \
                #         + 'votes:' + votes.get_text() + '\n') 

                f.write(ques.get_text() + pure_answer_text + '\n')
                idx += 1
        
        print(keyword, 'complete.', 'total {0} line datas'.format(str(idx)))

        

if __name__ == '__main__':
    zh = ZhiHu()
    zh.login()

    urls = {}
    file_path = os.getcwd() + '\\' + 'urls'
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().split(',')
            urls[line[0]] = line[1]

    for keyword, url in urls.items():
        zh.access(keyword, url)
        time.sleep(3)


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