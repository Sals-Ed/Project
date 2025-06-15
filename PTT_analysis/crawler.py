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

# get the article urls from the soup object
def get_topic_url(soup: BeautifulSoup) -> bool:
    # process some html tags to get the target we want
    articles = soup.find_all("div", {"class": "r-ent"})
    for article in articles:
        if article.find("div", {"class": "title"}):
            date = article.find("div", {"class": "date"}).text
            try:
                article_urls.append(article.find("a").get("href"))
            except: continue

# the main function to crawl the articles      
def Crawler(limit: int) -> list:
    print(">>>加載開始，請稍候...")
    page = "https://www.ptt.cc/bbs/HatePolitics/index4000.html"
    while True:
        # get the info from current page
        soup = site_visit(page)
        get_topic_url(soup)
        print(f"{page}已加載完成，當前共計入{len(article_urls)}篇文章") # to inform myself it is working 
        limit -= 1
        if limit <= 0: break

        # find the next page url
        buttons = soup.find_all("a", {"class": "btn wide"})
        next_page = [button for button in buttons if button.string=="‹ 上頁"][0].get("href")
        page = "https://www.ptt.cc" + next_page

        time.sleep(random.randint(0, 1))
    print(f">>>PTT政治板-指定範圍所有文章網址已儲存完畢")
    return article_urls

# # test
# test = Crawler(5)
# for i in test:
#     print(i)
#     time.sleep(0.03)
