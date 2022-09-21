from random import randint

import jieba
import numpy as np
import requests
from PIL import Image
from bs4 import BeautifulSoup
from wordcloud import WordCloud

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "accept-encoding": "deflate"
}

with open("word.txt", "w", encoding="utf-8-sig") as c:
    c.close()


def get_cid():
    print("请输入哔哩哔哩视频BV号。列如：BV1GJ411x7h7：")
    get_bv = input("")

    bv_json = requests.get(f"https://api.bilibili.com/x/player/pagelist?bvid={get_bv}&jsonp=jsonp",
                           headers=headers, timeout=3).json()
    cid = bv_json["data"][0]["cid"]
    return cid


def get_dm(cid):
    dm_text = requests.get(f'http://comment.bilibili.com/{cid}.xml', headers=headers)
    dm_text.encoding = 'utf-8'
    xhtml = BeautifulSoup(dm_text.text, features="xml")
    # print(xhtml.prettify())
    d_list = xhtml.find_all("d")
    for dm in d_list:
        with open("word.txt", "a+", encoding="utf-8-sig") as f:
            f.write(f"{dm.text}\n")
    return "弹幕获取成功！！！"


def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = randint(60, 300)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(randint(30, 300)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)


def ciyun():
    with open("word.txt", "r", encoding="utf-8-sig") as t:
        txt = t.read()
    words = jieba.lcut(txt)
    txt = ''.join(words)
    mask = np.array(Image.open("bg.png"))


    wordcloud = WordCloud(background_color="black",
                          width=2048,
                          height=2048,
                          max_words=300,
                          min_font_size=10,
                          max_font_size=120,
                          color_func=random_color_func,
                          mask=mask,
                          contour_width=4,
                          contour_color='white',
                          font_path="msyh.ttf"
                          ).generate(txt)
    wordcloud.to_file('bg_词云图.png')


if __name__ == "__main__":
    try:
        cid = get_cid()
        print(get_dm(cid))
        ciyun()
        print("制作完成！！！")
    except:
        print("BV号不存在！！！")
