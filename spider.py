import requests
import re
from bs4 import BeautifulSoup
import pandas
main_url=['https://tv.cctv.com/','http://report.12377.cn:13225/toreportinputNormal_anis.do','http://www.piyao.org.cn/yybgt/index.htm','http://downpack.baidu.com/baidunews_AndroidPhone_1014720b.apk','https://news.baidu.com/','https://www.baidu.com/','http://tieba.baidu.com/','https://zhidao.baidu.com/','http://music.baidu.com/','http://image.baidu.com/','http://v.baidu.com/','http://map.baidu.com/','http://wenku.baidu.com/','http://news.baidu.com/']

def create_new():
    dataframe = pandas.DataFrame(columns=['link','title','text', 'children'],dtype='str')
    dataframe['link']=''
    dataframe['text'] = ''
    dataframe['title'] = ''
    dataframe['children'] = ''
    return dataframe

def get_html(cm):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        r = requests.get(cm,headers=header,timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except:
       return "产生异常"

def normal_search_634(url):
    global dataframe
    a_link=[]   #保存A标签
    url_link=[] #保存获取的链接
    title_set=set()
    getten_url=set()#保存已经访问过的链接
    run_url=[]
    run_url.append(url)
    dataframe=create_new()
    i = j = w = 0
    while(i<10000 and len(run_url)!=0):
        url_link.clear()
        url=run_url.pop(0)
        if('baidu' not in url):
            continue
        html=get_html(url)
        if(html=="产生异常"):
            continue
        linksoup = BeautifulSoup(html.text,"html.parser")
        try:
            title = str(linksoup.find('head').find_next('title'))[7:-8]#获取标题
            if(len(title)==0 or title in title_set): #判断标题是否无或者以存在
                continue
            a_link = linksoup.find_all("a",href=True)   #找到所有a标签
            for link in a_link:#去除视频链接
                span=link.find('span')
                if(span!=None):
                    if(span.get('class')!=None):
                        x=span.get('class')
                        if(len(x)>0):
                            if("related-video-icon" in x):
                                continue
                href_link = link.get('href')
                if(href_link[-3:]=='apk'):#去除下载链接
                    continue
                if(len(href_link)>5):#去除链接过少
                    if(href_link[0]=='/' and href_link[1]!='/'):
                         href_link=url[:-1]+href_link
                    elif(href_link[0]=='/' and href_link[1]=='/'):
                        continue
                    if(href_link.find('http')==-1):#去除无http的链接
                        continue
                    if(href_link not in main_url):
                        url_link.append(href_link)
            getten_url.add(url)
            title_set.add(title)
            text=re.findall("[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]",html.text)
            text="".join(text)
            if(len(text)<100):
                continue
            if(len(url_link)<5):
                continue
            s = {'link':url,'title':title,'children':url_link,'text':text}
            dataframe = dataframe.append(s,ignore_index=True)
            for url_on in url_link:
                if((url_on not in getten_url) and (url_on not in run_url)):
                    run_url.append(url_on)
            i+=1
            print('已爬取',i,'待爬取队列链接数量：',len(run_url),'当前链接为：'+url)
            # if(i%200==0):
            #     dataframe.to_csv("page"+".csv",encoding='utf_8_sig')
            #     # dataframe=create_new()
        except:
            print('error')

url=('https://baijiahao.baidu.com/s?id=1687656563306385472')
normal_search_634(url)