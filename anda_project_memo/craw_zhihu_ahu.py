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
    
    def access(self, url, keyword):
        cookie = self.driver.get_cookies()
        time.sleep(2)
        
        self.driver.get(url)
        time.sleep(5)

        print('Get from: ' + url)
        print('About: ' + keyword)
        cnt = 1
        while True:
            try:
                self.driver.find_element_by_css_selector('.zg-btn-white.zu-button-more').click()
                time.sleep(2)
                print('click:' + str(cnt))
                cnt += 1
            except:
                break
    
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        with open(keyword + '_result', 'w', encoding='utf-8') as f:

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
                pure_answer_text = re.sub(r'<.*?>', '', answer_text)
                f.write('index:' + str(idx) + ',' \
                        + 'question:' + ques.get_text() + ',' \
                        + 'author:' + ('匿名用户' if author is None else author.get_text()) + ',' \
                        + 'answer:' + pure_answer_text + ',' \
                        + 'votes:' + votes.get_text() + '\n') 
                idx += 1


if __name__ == '__main__':
    zh = ZhiHu()
    zh.login()
    short_ahu_url = 'https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%A4%A7'
    zh.access(short_ahu_url, '安大')

    ahu_url = 'https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6'
    zh.access(ahu_url, '安徽大学')