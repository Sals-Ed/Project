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

    def analyze(self)-> dict:
        result = {"標題": "",
                  "作者": "",
                  "日期": "",
                  "綱要": "",
                  "評論風向": "",
                  "氛圍": "",
                  "網軍介入可能性": float()}
        result = environment.chain.invoke(f"""給定一篇文章的資訊，請依照該格式[{result}]分析並填入這篇文章的各種要素
            綱要必須濃縮在30字內，風向請用正面、負面、中立來表示，氛圍請選和諧、正常、緊張、對立，網軍介入可能性請用0到1之間的浮點數來表示。
            輸出字典列表物件，請注意！！！我只要上述的輸出就好，絕不要輸出其他說明。文章資訊:{self.__dict__}""")
        try:    
            analysis = eval(result)
        except:
            print(">>>分析過程中發生錯誤，跳過本文章分析。")
            return False
        print(">>>文章分析完成。")
        return analysis