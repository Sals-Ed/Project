import analysis
import crawler
import integration

# # crawl the articles from PTT
# articles = crawler.Crawler(5)
# count = 0 # count the number of articles analyzed
# for url in articles:
#     # data analyze the article
#     article = analysis.Article("https://www.ptt.cc" + url)
#     response = article.analyze()
#     count += 1
#     print(f"@@@已分析{count}篇文章@@@")
#     print(response)
#     with open(f"article_{count}.txt", "w", encoding="utf-8") as f:
#         f.write(str(response)) # raw data
#     vector = integration.extract(response) 

#     with open(f"vector_{count}.txt", "w", encoding="utf-8") as f:
#         f.write(str(vector)) # vector data

import time

#plot the relationship of the analysis data
data = []
for i in range(1, 61):
    with open(f"vector_{i}.txt", "r", encoding="utf-8") as f:
        content = f.read()
        content = eval(content)
        try:
            content = (eval(content[0]), eval(content[1]), eval(content[2]))
        except:
            continue
    data.append(content)
integration.plot(data)