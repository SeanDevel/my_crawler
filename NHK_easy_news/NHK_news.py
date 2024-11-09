import re
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path


class NHK_News:
    def __init__(self, url, start, end):
        self.url = url
        self.start = start
        self.end = end
        self.raw_news_list = self.get_raw_news()

    def text_list_to_latex_ruby(self, text_list: list, suffix: str):
        latex_code = ""
        i = 0
        while (i < len(text_list)):
            kanji_pattern = r'[\u4E00-\u9FFF]'
            if re.match(kanji_pattern, text_list[i]):
                latex_code += f"\\ruby{suffix}{{{text_list[i]}}}{{{text_list[i+1]}}}"
                i += 1
            else:
                latex_code += text_list[i]
            i += 1
        return latex_code.strip()

    def raw_to_latex_ruby(self, raw, suffix):
        soup = BeautifulSoup(raw, 'html.parser')
        text_list = soup.find_all(string=True)
        return self.text_list_to_latex_ruby(text_list, suffix)

    def get_page_by_webdriver(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        return driver.page_source

    def get_raw_title_and_content(self, news_url):
        soup = BeautifulSoup(
            self.get_page_by_webdriver(news_url), 'html.parser')
        title = soup.find("h1", class_="article-title")
        paragraphs = soup.select(
            "div.l-container main.l-main.easy-news article.easy-article div.article-body p")
        date = soup.find('p', id="js-article-date").get_text()
        main = [str(p) for p in paragraphs]
        return {'title': str(title), 'main_para': main, 'date': date, 'url': news_url}
        # with open('content.txt', 'a', encoding='utf-8') as f:
        #     f.write(''.join(str(child) for child in title.contents) + '\n')
        #     f.write(content + '\n')
        #     f.write('\n-------------\n\n')

    def get_raw_news(self):
        if self.start > self.end:
            print("Start must be less than or equal to end.")
            return
        soup = BeautifulSoup(
            self.get_page_by_webdriver(self.url), 'html.parser')
        # response = requests.get(url)
        # Step 2: Locate the <section id="js-news-list"> and find the 4th <article class="news-list__item">
        news_soup = soup.find_all("article", class_="news-list__item")
        raw_news_list = []
        for i in list(range(self.start-1, self.end))[::-1]:
            news_link = news_soup[i]
            a_tag = news_link.find("a", href=True)
            if a_tag:
                news_url = a_tag['href']
                news = self.get_raw_title_and_content(
                    'https://www3.nhk.or.jp'+news_url)
                raw_news_list.append(news)
            else:
                print("Out of range.")
        # self.raw_news_list = raw_news_list
        return raw_news_list

    def text_removing_rt(self, raw):
        soup = BeautifulSoup(raw, 'html.parser')
        # Find all <rt> elements and remove them
        for rt_tag in soup.find_all('rt'):
            rt_tag.decompose()
        return ''.join(soup.find_all(string=True)).strip()

    def raw_news_to_latex(self):
        raw_news_list = self.raw_news_list
        for i, news in enumerate(raw_news_list):
            title = news['title']
            latex_title = self.raw_to_latex_ruby(title, 'title')
            origin_title = self.text_removing_rt(title)

            main_list = news['main_para']
            latex_main = ''
            origin_main = ''

            for j, main in enumerate(main_list):
                latex_main += self.raw_to_latex_ruby(main, 'main')
                origin_main += self.text_removing_rt(main)
                if j == len(main_list)-1:
                    latex_main += '\n'
                    origin_main += '\n'
                else:
                    latex_main += '\n\n'
                    origin_main += '\n\n'

            save_text_path = Path('./news_text')
            if not save_text_path.exists():
                save_text_path.mkdir()

            news_date = news['date'].split(" ")[0]

            current_datetime = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
            filename = f'news_{news_date}_{i+1}_[{current_datetime}].txt'
            
            filepath = save_text_path.joinpath(filename)
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(
                    '\\addcontentsline{toc}{subsection}{'+origin_title+'}\n')
                f.write('\n'+news_date+'\n\n')
                f.write('\\begin{titleJap}\n')
                f.write(latex_title + '\n')
                f.write('\\end{titleJap}\n\n')
                f.write('\\begin{mainJap}\n')
                f.write(latex_main)
                f.write('\\end{mainJap}\n\n')
                f.write('\\hfill\n')
                f.write('\\pdfcomment{'+news['url']+'}\n\n')
                f.write('\\newpage\n\n')
                f.write('\\begin{titleZh}\n\n')
                f.write('\\end{titleZh}\n\n')
                f.write('\\begin{mainZh}\n\n')
                f.write('\\end{mainZh}\n\n')
                f.write('\\newpage\n\n')
                f.write(origin_title + '\n\n')
                f.write(origin_main)

    # def raw_news_to_origin(self):
    #     raw_news_list = self.raw_news_list
    #     for i, news in enumerate(raw_news_list):
    #         title = news['title']
    #         origin_title = self.text_removing_rt(title)

    #         main_list = news['main_para']
    #         origin_main = ''
    #         for main in main_list:
    #             origin_main += self.text_removing_rt(main)+'\n\n'

    #         date = news['date'].split(" ")[0]
    #         with open(f'news-origin_{date}_{i+1}.txt', 'a', encoding='utf-8') as f:
    #             f.write('\\begin\{titleZh\}\n')
    #             f.write(origin_title + '\n\n')
    #             f.write('\\end\{titleZh\}\n\n')
    #             f.write('\\begin\{mainZh\}\n')
    #             f.write(origin_main + '\n')
    #             f.write('\\end\{mainZh\}\n')


if __name__ == "__main__":
    url = "https://www3.nhk.or.jp/news/easy/"
    start = 1
    end = 4
    news = NHK_News(url, start, end)
    news.raw_news_to_latex()
    # news.raw_news_to_origin()


'''
总结：面向对象的优势
一些数据需要在多处方法种作为参数，将这些数据存储在对象种能够简化代码，提高代码的可读性。
例如爬虫程序中有多个方法需要访问同一类数据，这些数据需要在多处方法种存储，将这些数据存储在对象种能够简化代码。

get_page_by_webdriver(url)
get_raw_news(url, start, end)
'''
