import pickle
import time

import requests
from bs4 import BeautifulSoup
from newspaper import Config, Article
import nltk

from data import *


config = Config()
config.request_timeout = 10



def get_hindu_news_urls():
    hindu_news_urls = []
    page = 880
    while page >= 90:
        base_url = "https://www.thehindu.com/search/?q=migrant&order=DESC&sort=publishdate&page={}".format(page)
        hindu_news_urls.append(base_url)
        page -= 1
    news_urls = {}
    news_urls['Hindu'] = hindu_news_urls
    hindu_article_links = []
    for url in hindu_news_urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        for li in soup.find_all('a', class_='story-card75x1-text'):
            hindu_article_links.append(li.get('href'))
    hindu_articles = open("data/HinduUrls.pickle", "wb")
    pickle.dump(hindu_article_links, hindu_articles)
    hindu_articles.close()
    return hindu_article_links

def get_hindu_articles(hindu_article_links):
    article_info = {}
    article_text = {}
    for idx in range(len(hindu_article_links)):
        article = Article(hindu_article_links[idx], config=config)
        article.download()
        article.parse()
        article.nlp()
        for key, val in article.meta_data.items():
            if key == 'publish-date':
                date = (str(val)).split('T')[0]
        article_info[idx] = {'Date': date, 'Keywords': article.keywords, 'Summary': article.summary}
        article_text[idx] = {'Date': date, 'Text': article.text}
    info = open("data/HinduNewsArticleInfo.pickle", "wb")
    pickle.dump(article_info, info)
    info.close()
    text = open("data/HinduNewsArticleText.pickle", "wb")
    pickle.dump(article_text, text)
    text.close()

def get_hindustan_times_urls():
    ht_news_urls = ["https://www.hindustantimes.com/topic/migrant", "https://www.hindustantimes.com/topic/migrant/page-2"]
    base_url = "https://www.hindustantimes.com"
    ht_news_article_links = []
    for url in ht_news_urls:
        agent = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(url, headers=agent)
        soup = BeautifulSoup(r.content, 'lxml')
        for li in soup.find_all('h2', class_='hdg3'):
            full_link = base_url + li.a.get('href')
            ht_news_article_links.append(full_link)
    ''' Additional 2 article links from April Hindustan Times '''
    ht_news_article_links.append('https://www.hindustantimes.com/india-news/calls-for-free-ration-grow-as-migrants-fight-hunger/story-PGYIUFYtkQpSHqnpf8dC2I.html')
    ht_news_article_links.append('https://www.hindustantimes.com/editorials/the-dilemma-with-migrants/story-2MKuKmHnYGYkdx7kk1zg1O.html')
    ht_news = open("data/HTUrls.pickle", "wb")
    pickle.dump(ht_news_article_links, ht_news)
    ht_news.close()
    return ht_news_article_links

def get_hindustan_times_articles(ht_news_article_links):
    HT_article_info = {}
    HT_article_text = {}
    for idx in range(len(ht_news_article_links)):
        article = Article(ht_news_article_links[idx], config=config)
        article.download()
        article.parse()
        article.nlp()
        HT_article_info[idx] = {'Date': article.publish_date.date(), 'Keywords': article.keywords, 'Summary': article.summary}
        HT_article_text[idx] = {'Date': article.publish_date.date(), 'Text': article.text}
    info_HT = open("data/HTNewsArticleInfo.pickle", "wb")
    pickle.dump(HT_article_info, info_HT)
    info_HT.close() 
    text_HT = open("data/HTNewsArticleText.pickle", "wb")
    pickle.dump(HT_article_text, text_HT)
    text_HT.close()

def get_NDTV_articles():
    f = open('data/NDTVurls.pickle', 'rb')
    ndtv_news_urls = pickle.load(f)
    f.close()
    nltk.download('punkt')
    NDTV_article_info = {}
    NDTV_article_text = {}
    for idx in range(len(ndtv_news_urls)):
        article = Article(ndtv_news_urls[idx], config=config)
        try:
            article.download()
            article.parse()
            article.nlp()
            for key, val in article.meta_data.items():
                if key == 'publish-date':
                    date = (str(val)).split('T')[0]
            NDTV_article_info[idx] = {'Date': date, 'Keywords': article.keywords, 'Summary': article.summary}
            NDTV_article_text[idx] = {'Date': date, 'Text': article.text}
        except:
            print("Parsing failed for ", ndtv_news_urls[idx])
    info = open("data/NDTVArticleInfo.pickle", "wb")
    pickle.dump(NDTV_article_info, info)
    info.close()
    text = open("data/NDTVArticleText.pickle", "wb")
    pickle.dump(NDTV_article_text, text)
    text.close()