import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class Crawl():
    def __init__(self, search_word, url_front, url_back, pages):
        self.search_word = search_word
        self.url_front = url_front
        self.url_back = url_back
        self.pages = pages
    
    def crawl_website(self):

        news_full = pd.DataFrame(columns={"page", "title", "url", "date", "desc"})

        for i in range (0,self.pages):
            url_full = self.url_front + str(i) + self.url_back
            print(i)
            time.sleep(1)

            res = requests.get(url_full)
            soup = BeautifulSoup(res.content, features="html.parser")
            table = soup.find_all('a', {"class": "news_tit"})
            date = soup.find_all('span', {"class": "info"})
            desc = soup.find_all('a', {"class": "api_txt_lines"})    
            
            page = i
            page_list = []
            number_list = []
            title_list = []
            hyperlink_list = []
            desc_list = []
            date_list = []

            news_full_add = pd.DataFrame(columns={"page", "title", "url", "date", "desc"})
            
            for i in range(0, len(table)):
                page_list.append(page)
                number_list.append(i)
                title_list.append(table[i].text) 
                hyperlink_list.append(table[i]['href'])
                desc_list.append(desc[i].text)
                date_list.append(date[i].text)

            news_full_add['page'] = page_list
            news_full_add['title'] = title_list
            news_full_add['url'] = hyperlink_list
            news_full_add['desc'] = desc_list
            news_full_add['date'] = date_list
        
            news_full = pd.concat([news_full, news_full_add])

        news_full['search_word'] = self.search_word

        news_full = news_full[['search_word', 'page', 'date', 'title', 'desc', 'url']]
        return news_full
