from bs4 import BeautifulSoup


html='''
<p><span class="color4"><ruby>7日<rt>なのか</rt></ruby></span><span class="colorB">は</span><span class="color0"><ruby>立冬<rt>りっとう</rt></ruby></span><span class="colorB">です</span><span class="colorB">。</span><span class="color0"><ruby>立冬<rt>りっとう</rt></ruby></span><span class="colorB">は</span><span class="color3"><ruby>昔<rt>むかし</rt></ruby></span><span class="colorB">から</span><span class="color4"><ruby>冬<rt>ふゆ</rt></ruby></span><span class="colorB">が</span><span class="color4"><ruby>始<rt>はじ</rt></ruby>まる</span><span class="color3"><ruby>日<rt>ひ</rt></ruby></span><span class="colorB">だ</span><span class="colorB">と</span><span class="color4"><ruby>言<rt>い</rt></ruby>わ</span><span class="colorB">れ</span><span class="colorB">て</span><span class="color4">い</span><span class="colorB">ます</span><span class="colorB">。</span><span class="color4"><ruby>7日<rt>なのか</rt></ruby></span><span class="color4"><ruby>朝<rt>あさ</rt></ruby></span><span class="colorB">は</span><span class="color3">いろいろ</span><span class="colorB">な</span><span class="color4"><ruby>所<rt>ところ</rt></ruby></span><span class="colorB">で</span><span class="colorB">、</span><span class="color4"><ruby>今<rt>いま</rt></ruby></span><span class="colorB">の</span><span class="color3"><ruby>季節<rt>きせつ</rt></ruby></span><span class="colorB">になって</span><span class="colorB">から</span><span class="color4">いちばん</span><span class="color4"><ruby>寒<rt>さむ</rt></ruby>く</span><span class="color4">なり</span><span class="colorB">ました</span><span class="colorB">。</span><span class="colorL"><ruby>北海道<rt>ほっかいどう</rt></ruby></span><span class="colorB">の</span><span class="colorL"><ruby>函館市<rt>はこだてし</rt></ruby></span><span class="colorB">と</span><span class="colorL"><ruby>室蘭市<rt>むろらんし</rt></ruby></span><span class="colorB">では</span><span class="colorB">、</span><span class="color4"><ruby>初<rt>はじ</rt></ruby>め</span><span class="colorB">て</span><span class="color4"><ruby>雪<rt>ゆき</rt></ruby></span><span class="colorB">が</span><span class="color4"><ruby>降<rt>ふ</rt></ruby>り</span><span class="colorB">ました</span><span class="colorB">。</span></p>
'''

date_html='''
<p class="article-date" id="js-article-date">2024年11月6日 19時52分</p>
'''

def remove_rt(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    # Find all <rt> elements and remove them
    for rt_tag in soup.find_all('rt'):
        rt_tag.decompose()
    return ''.join(soup.find_all(string=True))

# text = remove_rt(html)

# print(text)
soup = BeautifulSoup(date_html, 'html.parser')
date = soup.find('p', id="js-article-date").get_text()
print(date)