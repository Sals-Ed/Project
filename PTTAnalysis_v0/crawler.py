import requests
import time
import random
from bs4 import BeautifulSoup

# store ptt article urls
article_urls = [] 

# get the source code of a site
def site_visit(url: str) -> BeautifulSoup:
    headers = { # simulate a real user visit
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        }
    content = requests.get(url, headers=headers)
    soup = BeautifulSoup(content.text, "html.parser") # turn the raw content into a format that easy to use
    return soup

# designate a specific time range to get articles
def date_check(date: str, stop: int) -> bool:
    if int(date[3:]) >= stop:
        return True
    else:
        return False

# get the article urls from the soup object
def get_topic_url(soup: BeautifulSoup, stop: int) -> bool:
    # process some html tags to get the target we want
    articles = soup.find_all("div", {"class": "r-ent"})
    for article in articles:
        if article.find("div", {"class": "title"}):
            date = article.find("div", {"class": "date"}).text
            if not date_check(date, stop):
                return False
            if article.find("a"):
                article_urls.append(article.find("a").get("href"))
    return True

# the main function to crawl the articles      
def Crawler(stop: int) -> list:
    print(">>>加載開始，請稍候...")
    page = "https://www.ptt.cc/bbs/hatepolitics/index3995.html"
    while True:
        # get the info from current page
        soup = site_visit(page)
        flag = get_topic_url(soup, stop)
        if not flag: break # out the the time range? boom!!!

        # find the next page url
        buttons = soup.find_all("a", {"class": "btn wide"})
        next_page = [button for button in buttons if button.string=="‹ 上頁"][0].get("href")
        print(f"{next_page}已加載完成，當前共計入{len(article_urls)}篇文章") # to inform myself it is working 
        page = "https://www.ptt.cc" + next_page

        time.sleep(random.randint(0, 2))
    print(f">>>PTT政治板-5月{stop}日至5月31日上午之所有文章網址已儲存完畢")
    return article_urls