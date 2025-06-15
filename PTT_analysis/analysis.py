import crawler
import environment

# cut the article into the multiple variables
class Article:
    def __init__(self, url: str):
        print(">>>開始擷取文章資訊...")
        # I dont know how to annotate this, I used devtools by clicking f12
        # Then I can move the mouse to detect the element I want
        # Finally I can analyze the article by these html tags
        soup = crawler.site_visit(url) 
        source_info = soup.find_all("div", {"class": "article-metaline"})
        self.url = url
        self.title = source_info[1].find("span", {"class": "article-meta-value"}).text
        self.author = source_info[0].find("span", {"class": "article-meta-value"}).text
        self.date = source_info[2].find("span", {"class": "article-meta-value"}).text
        self.content = soup.find("div", {"id": "main-content"})
        for tag in self.content.find_all("div", {"class": "article-metaline"}):
            tag.decompose()
        self.content = self.content.text.split("--")[0].strip()
        self.comments = soup.find_all("div", {"class": "push"})
        self.comments = [comment.text.strip() for comment in self.comments]
        print(">>>文章資訊擷取完成，開始分析文章內容...")

    def summary(self) -> str:  
        prompt = environment.ChatPromptTemplate.from_messages([
            ("system", "你是一名專業的文本分析師"),
            ("human", "請提煉出該文章之綱要,並且避免評判與情緒化用詞,以50字繁體中文內為限"),
            ("human", "注意,輸出只需綱要,絕對不要給我額外說明,總結以下文本:{text}")
        ])
        return (prompt | environment.chain).invoke({"text": self.content})
        

    def comment_tendency(self) -> float:
        prompt = environment.ChatPromptTemplate.from_messages([
            ("system", "你是一名專業的輿情分析師"),
            ("human", "請根據整體留言版內容打一個分數,請打分至小數點後三位,越新的留言越有參考價值"),
            ("human", "0(留言者意見極度分散)~1(留言者意見極度集中),只要輸出分數,絕對不要額外說明,留言如下：{text}")
        ])
        result = (prompt | environment.chain).invoke({"text": self.comments})
        print(f">>>評論風向分析完成->{result}")
        return result

    def atmosphere(self) -> float:
        prompt = environment.ChatPromptTemplate.from_messages([
            ("system", "你是一名專業的輿情分析師"),
            ("human", "請根據整體留言版內容打一個分數,請打分至小數點後三位"),
            ("human", "0(留言者用詞極度極端)~1(留言者意見極度理性),只要輸出分數,絕對不要額外說明,留言如下:{text}")
        ])
        result = (prompt | environment.chain).invoke({"text": self.comments})
        print(f">>>留言氛圍分析完成->{result}")
        return result

    def troll_evaluation(self) -> float:
        prompt = environment.ChatPromptTemplate.from_messages([
            ("system", "你是一名專業的輿情分析師"),
            ("human", "請根據整體留言版內容打一個分數,請打分至小數點後三位"),
            ("human", "分析留言意有所指?誘導性?存在帶風向?促成暗示?0(留言板完全都是網軍)~1(留言板完全是表達自我意見的用戶),只要輸出分數,絕對不要額外說明,留言如下：{text}")
        ])
        result = (prompt | environment.chain).invoke({"text": self.comments})
        print(f">>>網軍評估分析完成->{result}")
        return result

    def analyze(self)-> dict:
        result = {"標題": "",
                  "作者": "",
                  "日期": "",
                  "綱要": "",
                  "評論風向": 0.0,
                  "氛圍": 0.0,
                  "網軍介入可能性": 0.0}
        result["標題"] = self.title
        result["作者"] = self.author
        result["日期"] = self.date
        result["綱要"] = self.summary()
        result["評論風向"] = self.comment_tendency()
        result["氛圍"] = self.atmosphere()
        result["網軍介入可能性"] = self.troll_evaluation()
        return result

# data = Article("https://www.ptt.cc/bbs/HatePolitics/M.1748586358.A.8A2.html")
# data = data.analyze()
# print(data)
