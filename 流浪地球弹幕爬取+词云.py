import requests
from bs4 import BeautifulSoup
import jieba
import wordcloud
from imageio import imread 


def getXMLText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

    
def parsePage(filetxt,xml):
    try:
        soup = BeautifulSoup(xml, "html.parser")
        f = open("流浪地球弹幕.txt",'a',encoding='UTF-8')
        for d in soup.find_all('d'):
            f.write(d.text)
            f.write('\n')
            print(d.text)
        f.close()

    except:
        return ""


def drawWordCloud(filetxt):
    mask_color = imread("地球.jpg")
    with open (filetxt,'r',encoding='UTF-8') as f:
        t = f.read()
        print("-"*15)
        ls = jieba.lcut(t.replace("觉得",""))
        
        txt = " ".join(ls)
        w = wordcloud.WordCloud(font_path = "msyh.ttc",\
                        width = 1000,\
                        height = 800,\
                        background_color = "white",\
                        mask = mask_color)

        w.generate(txt)
        image_colors = wordcloud.ImageColorGenerator(mask_color)
        w.recolor(color_func=image_colors)
        
        w.to_file("流浪地球词云.png")
    pass

def main():
    # 75517666 av43070893_火锅大王
    # 75395476 av42999745_木鱼水心
    # 76148742 av43448442_歪果仁研究协会
    oid = '76148742'
    filetxt = '流浪地球弹幕.txt'
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+oid
    try:
        xml = getXMLText(url)
        parsePage(filetxt,xml)
    except:
        print("爬取错误")

    drawWordCloud(filetxt)

main()
