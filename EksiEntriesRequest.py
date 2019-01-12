import pycurl
from io import BytesIO
from bs4 import BeautifulSoup
import requests


def fetch_entries(baslik):
    url = 'https://eksisozluk.com/'
    path = url+"?q="+baslik

    response = requests.get(path, headers={"User-Agent":"Mozilla/5.0"})
    path = response.url

    page_last = get_response(path).find("div", class_="pager").attrs['data-pagecount']

    for i in range(1, int(page_last)):
        path_pagenum = path+"?p="+str(i)
        page = get_response(path_pagenum).find_all("div", class_="content")
        with open('input.txt', 'a+') as f:
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


#fetch_entries('ttnet')