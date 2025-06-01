import analysis
import crawler
import integration

# crawl the articles from PTT
articles = crawler.Crawler(31)
result = []
count = 0 # count the number of articles analyzed
for url in articles:
    if count > 100: break
    if count % 5 == 0:
        print(result)
        # cut the result into 5 articles scale, or if somewhere wrong
        # my computer will have to run again, and it is very hot now
        with open(f"raw_{count//5}.txt", "w", encoding="utf-8") as f:
            f.write(str(result)) # raw data
        result = [integration.convert(r) for r in result]
        with open(f"vector_{count//5}.txt", "w", encoding="utf-8") as f:
            f.write(str(result)) # vector data
        result = []
    # data analyze the article
    article = analysis.Article("https://www.ptt.cc" + url)
    temp = article.analyze()
    if temp is False: continue
    count += 1
    result.append(temp[0])
    print(f"@@@已分析{count}篇文章@@@")

# for i in range(20):
#     data = []
#     with open(f"result_{i}.txt", "r", encoding="utf-8") as f:
#         data.extend(eval(f.read()))
# integration.plot(data)