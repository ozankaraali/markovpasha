import os
import pycurl
from io import BytesIO
from bs4 import BeautifulSoup
import requests
import markovify
import nltk
import re


class NaturalLanguageText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def fetch_entries(baslik):
    url = 'https://eksisozluk.com/'
    path = url+"?q="+baslik

    exists = os.path.isfile('./data/'+baslik+'.txt')
    if not exists:
        response = requests.get(path, headers={"User-Agent":"Mozilla/5.0"})
        path = response.url

        page_last = get_response(path).find("div", class_="pager").attrs['data-pagecount']

        for i in range(1, int(page_last)):
            path_pagenum = path+"?p="+str(i)
            page = get_response(path_pagenum).find_all("div", class_="content")
            with open('./data/'+baslik+'.txt', 'a+') as f:
                for e in page:
                    res_str = e.get_text()
                    f.write("%s\n" % res_str[6:len(res_str)-4])


def get_response(path):
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, path)

    response_bytes = BytesIO()

    curl.setopt(pycurl.WRITEFUNCTION, response_bytes.write)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, 5)

    curl.perform()

    html_response = response_bytes.getvalue().decode('UTF-8')

    return BeautifulSoup(html_response, "lxml")