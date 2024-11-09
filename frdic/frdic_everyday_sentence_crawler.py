from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import time
from datetime import datetime
from pathlib import Path


class FrenchSentenceCrawler:
    def __init__(self, url):
        self.url = url
        self.page_source = None
        self.daytime = None
        self.taget_url = None
        self.sentence = None
        self.translation = None
        self.analysis = None
        self.crawler()

    def crawler(self):
        """
        Uses Selenium to navigate to the page and extract the target URL
        and source HTML.

        Sets the following attributes:
        - taget_url: the URL of the target page
        - page_source: the HTML source of the page

        Notes:
        - The target page is extracted by finding the a.voiceText element
          within the div#qod element.
        - The page_source is extracted after navigating to the target page.
        - If there is an error during navigation, the function prints an error
          message and exits the program.
        """
        driver = webdriver.Chrome()
        driver.get(url)
        try:
            target_url = driver.find_element(
                By.CSS_SELECTOR, "div#qod > a.voiceText").get_attribute("href")
            self.taget_url = target_url
            driver.get(target_url)
            # time.sleep(3)
            self.page_source = driver.page_source
        except Exception as e:
            print(f"Error navigating to div: {e}")
            driver.quit()
            exit()

    def build_content(self):
        """
        Extracts and sets the daytime, sentence, translation, and analysis
        from the page source HTML content.

        Utilizes BeautifulSoup to parse the HTML and extract relevant
        information based on specific CSS selectors and element IDs.

        Attributes:
        -----------
        self.daytime : str
            The extracted daytime text from the HTML.
        self.sentence : str
            The extracted sentence text from the HTML.
        self.translation : str
            The extracted translation text from the HTML.
        self.analysis : str
            The extracted analysis text from the HTML.

        Exceptions:
        -----------
        Prints an error message if there is an issue extracting text from
        the expected HTML elements.
        """
        soup = BeautifulSoup(self.page_source, 'html.parser')
        # date
        try:
            daytime = soup.select('div.header_info p.daytime')[0].text
            self.daytime = daytime
        except Exception as e:
            print(f"Error extracting text from div.header_info p.daytime: {e}")
        # sentence and translation
        try:
            senten_move_div = soup.find('div', id='senten_move')
            p_texts = [p.text.strip() for p in senten_move_div.find_all('p')]
            self.sentence = p_texts[0]
            self.translation = p_texts[1]
        except Exception as e:
            print(f"Error extracting text from div#senten_move: {e}")
        # analysis
        try:
            analysis_div = soup.find('div', class_='analysis')
            if analysis_div:
                an_info_div = analysis_div.find(
                    'div', class_='an-info info_fr')
                if an_info_div:
                    span_texts = [span.text.strip()
                                  for span in an_info_div.find_all('span')]
                    analysis = ''
                    for span_text in span_texts:
                        analysis += span_text+'\n'
                    self.analysis = analysis
        except Exception as e:
            print(
                f"Error extracting text from div.analysis div.an-info info_fr: {e}")

    def create_archive(self):
        """
        Create a directory with the current date and name of the sentence. 
        Then save each piece of content to a file with the same name as the sentence.
        """
        today_date = datetime.now().strftime('%Y-%m-%d')
        path = Path(f'./archive/{today_date}_{self.sentence}')

        if not path.exists():
            try:
                path.mkdir()
                print(f"Created folder: {path}")
            except Exception as e:
                print(f"Error creating folder: {e}")

        contents = {
            'daytime': (self.daytime, 2),
            'taget_url': (self.taget_url, 2),
            'sentence': (self.sentence, 1),
            'translation': (self.translation, 2),
            'analysis': (self.analysis, 1)
        }

        filename = f"{path}/{self.sentence}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for cont_name, (cont_value, line_breaks) in contents.items():
                    if cont_value:
                        f.write(f'{cont_value}'+'\n'*line_breaks)
                    else:
                        print(f"No {cont_name}.")
            print(f"Created text file: {filename}")
        except Exception as e:
            print(f"Error creating text file: {e}")


if __name__ == "__main__":
    url = "https://www.frdic.com/"
    crawler = FrenchSentenceCrawler(url)
    crawler.build_content()
    crawler.create_archive()
