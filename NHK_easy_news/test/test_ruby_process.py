from bs4 import BeautifulSoup
import re

# Read the text from the file
with open('content.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Get the second line of the text file
line = lines[1]

def text_list_to_letex_ruby(text_list: list, suffix: str):
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
    return latex_code

def paragraph_to_latex_ruby(paragraph, suffix):
    soup = BeautifulSoup(paragraph, 'html.parser')
    text_list = soup.find_all(string=True)
    return text_list_to_letex_ruby(text_list, suffix)


result = paragraph_to_latex_ruby(lines[5],'text')
print(result)


def title(line):

    soup = BeautifulSoup(line, 'html.parser')
    # Find all <ruby> elements
    ruby_elements = soup.find_all('ruby')

    latex_code = ""

    notationList = []

    for ruby in ruby_elements:
        kanji_text = ruby.get_text()
        hiragana = ruby.find('rt')
        if hiragana:
            hiragana_text = hiragana.get_text()
        notationList.append((kanji_text, hiragana_text))

    entire_text = soup.find_all(string=True)

    i = 0
    while (i < len(entire_text)):
        kanji_pattern = r'[\u4E00-\u9FFF]'

        if re.match(kanji_pattern, entire_text[i]):
            latex_code += f"\\ruby{{{entire_text[i]}}}{{{entire_text[i+1]}}}"
            i += 1
        else:
            latex_code += entire_text[i]
        i += 1
    print(latex_code)
    return latex_code
