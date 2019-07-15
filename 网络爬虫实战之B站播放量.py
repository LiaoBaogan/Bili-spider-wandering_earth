'''
目标：获取BILIBILI搜索页面的信息，提取视频名称及播放量
理解：B站的搜索接口及翻页的处理

搜索页：https://search.bilibili.com/all?keyword=流浪地球
第二页：https://search.bilibili.com/all?keyword=流浪地球&page=2
第三页：https://search.bilibili.com/all?keyword=流浪地球&page=3
播放量在:
#server-search-app > div.contain > div.body-contain > div > div.result-wrap.clearfix > \
ul.video-contain.clearfix > li:nth-child(1) > div > div.tags > span.so-icon.watch-num
技术路线：request-bs4
'''
import requests
from bs4 import BeautifulSoup
import bs4


def getHTMLText(url):

    cookies = {
        'buvid3': 'C4776336-2C8D-46FF-A657-D01D676BEB3F77426infoc',
        'LIVE_BUVID': 'AUTO1515481696951161',
        'sid': 'kwcuwnah',
        'DedeUserID': '86428130',
        'DedeUserID__ckMd5': '8a975e2aa5a3d003',
        'SESSDATA': '24ff4354%2C1550761779%2Ce5ae5111',
        'bili_jct': '58642c798d16441413af26f0ee5f5e03',
        'stardustvideo': '1',
        'CURRENT_FNVAL': '16',
        'rpdid': 'iwiqmmmowsdospqoxllqw',
        '_uuid': '46B166A4-7E94-45E8-B190-2E2AE815D40B73896infoc',
        'UM_distinctid': '16878a25940598-0d929d8677d087-b781636-144000-16878a259413df',
        'fts': '1548234975',
        'finger': '17c9e5f5',
        'CURRENT_QUALITY': '80',
        'im_notify_type_86428130': '0',
        'bp_t_offset_86428130': '218527665443023397',
        '_dfcaptcha': '78420e5fdc766ca64e7fa453bee9c3ca',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.bilibili.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    params = (
        ('keyword', '\u6D41\u6D6A\u5730\u7403'),
        ('from_source', 'banner_search'),
    )

    try:
        r = requests.get(url,timeout = 30,headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def parsePage(infolt,html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        for li in soup.find('ul',{"class":'video-contain'}).children:
            vname = li.find('a',{"class" : 'title'}).text
            vname = vname.replace('\n','')
            vname = vname.replace(' ','')
            vwatchnum =li.find('span',{"title" : '观看'}).text
            vwatchnum = vwatchnum.replace('\n','')
            vwatchnum = vwatchnum.replace(' ','')
            vdanmu = li.find('span',{"title" : '弹幕'}).text
            vdanmu = vdanmu.replace('\n','')
            vdanmu = vdanmu.replace(' ','')
            vup = li.find('span',{"title" : 'up主'}).text
            vup = vup.replace('\n','')
            vup = vup.replace(' ','')
            infolt.append([vname,vwatchnum,vdanmu,vup])
        
    except:
        print("")
            
def printVediosList(infolt):
    tplt = "{0:{4}<50}\t{1:{4}<10}\t{2:{4}<10}\t{3:{4}^10}" 
    print(tplt.format("视频名称","播放量","弹幕数","UP主",chr(12288)))
    for i in infolt:
        print(tplt.format(i[0],i[1],i[2],i[3],chr(12288)))

        
def main():
    vedios = "流浪地球"
    depth = 3
    start_url = "https://search.bilibili.com/all?keyword=" + vedios
    infolist = []
    for i in range(depth):
        try:
            url = start_url + "&page=" + str(i+1)
            html = getHTMLText(url)
            parsePage(infolist,html)
        except:
            continue
    printVediosList(infolist)

main()
