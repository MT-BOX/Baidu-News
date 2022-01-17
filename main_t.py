import jieba
import pandas
import math
from tqdm import tqdm
import pickle
import ZAIYAO
import os
import numpy
from tkinter import *
import tkinter as tk
import tkinter.messagebox
from PIL import ImageTk,Image

def pagerank_634():#计算pagerank
    link_page = pandas.read_pickle('link12000.pkl')
    pagelen = len(link_page)
    chudu = numpy.zeros(pagelen)#出度矩阵
    page = numpy.zeros((pagelen, pagelen))#邻接矩阵
    pr = numpy.zeros(pagelen)
    for i in range(pagelen):#pr初值
        pr[i] = 1
    for i in range(pagelen):#统计出度和邻接矩阵
        chudu[i] = len(link_page.loc[i]['children_index']) + 1
        for t in link_page.loc[i]['children_index']:
            page[int(t)][i] = 1
    d = 0.25
    ps = numpy.zeros(pagelen)
    while (True):#迭代求解
        for i in tqdm(range(pagelen)):
            ps[i] = 1 - d + d * sum(pr * page[i] / chudu)
        print(sum(pr))
        if (math.fabs(pr[1] - ps[1]) < 0.000001):#精确度
            break
        for i in range(pagelen):
            pr[i] = ps[i]

    dataframe =pandas.DataFrame([link_page['url'].values,pr], dtype='str').T
    dataframe.columns=['url','Pagerank']
    dataframe.to_csv('PageRanks.csv')

class Serach:#建索引和搜索类
    def __init__(self):  # 初始化参数，即得到待操作的文本
        self.da=pandas.read_pickle('Dao_index.pickle')
        self.link_page = pandas.read_pickle('link12000.pkl')
        self.pagelen = len(self.link_page)
        self.stopwords_file = "cn_stopwords.txt"
        self.stop_f = open(self.stopwords_file, "r", encoding='utf-8')
        self.stop_words = set()
        self.pagerank=pandas.read_csv('PageRanks.csv')
        for line in self.stop_f.readlines():
            self.stop_words.add(str(line[:-1]))
        self.keywords=[]
    def jiebcut_634(self):#分词
        content1=[]
        for content in tqdm(self.link_page['content'].values):
            xx = jieba.cut_for_search(content)#jieba搜索引擎分词
            tc=[]
            for xt in xx:#去停用词
                if(xt not in self.stop_words):
                    tc.append(xt)
            content1.append(",".join(tc))
        dataf=pandas.DataFrame(content1,columns=['words'])
        dataf.to_csv('Words.csv',encoding='utf_8_sig')
    def creat_daopai_634(self):#根据分词结果建立倒排索引
        data=pandas.read_csv('Words.csv')
        words_len=len(data)
        daoIndex=dict()
        for i in tqdm(range(words_len)):#建倒排
            tx=data.loc[i]['words'].split(',')
            for x in tx:
                try:
                    daoIndex[x].add(i)#字典存在则向集合添加元素
                except:
                    xu=set()#字典不存在则创建字典元素
                    xu.add(i)
                    daoIndex[x]=xu
        pickle.dump(daoIndex,open('./Dao_index.pickle','wb'))#将字典写进pkl文件
    def catch_634(self,text):#根据输入的关键词获取检索结果
        s=text
        xx=jieba.cut_for_search(s)#对搜索局进行分词
        self.keywords.clear()
        for x in xx:#去停用词
            if(x not in self.stop_words):
                self.keywords.append(x)
        print(self.keywords)
        a=set()
        for t in self.keywords:#检索字典求并集
            try:
                b=self.da[t]
                a=a|b
            except:
                pass
        print(a)
        message=[]
        for t in a:#生产摘要和关键词次数并将信息整合
            text=self.link_page.loc[t,'content']
            mains=ZAIYAO.zaiyao_634(text,self.keywords,40).getZAOYAO_634()
            main=mains[0]+'...'
            message.append([self.pagerank.loc[t]['url'],self.link_page.loc[t]['title'],main,self.link_page.loc[t,'label'],float(self.pagerank.loc[t]['Pagerank']),mains[1],t])
        message.sort(key = lambda x : (x[5],x[4]),reverse=True)#按关键词出现次数和pagerank进行排序
        return message[:100]
    def return_key(self):
        return self.keywords

message=[]
s=Serach()
key=''
flag=1
leave=0
end=0
page_len=0
keywords=[]
def main_te_634(serach_text):#信息检索主界面
    def serach(event):#搜索
        global key
        global page_len
        global end
        global leave
        global message
        global keywords
        key = entry_1.get()
        if(len(key)!=0):#对空进行处理
            message = s.catch_634(key)
            keywords=s.return_key()
            page_len=len(message)
            print(page_len)
            if(page_len%6==0):#获取页数
                end=int(page_len/6)
            else:
                end=int(page_len/6)+1
        leave=0
        window.destroy()
    def next_page(event):#下一页
        global leave
        leave+=1
        window.destroy()
    def hea_page(event):#上一页
        global leave
        leave-=1
        window.destroy()
    def first_page(event):#首页
        global leave
        leave=0
        window.destroy()
    def last_page(event):#尾页
        global leave
        leave=end-1
        window.destroy()
    def open_this(event,index):#打开网页
        ur='"C:/Program Files/Google/Chrome/Application/chrome.exe" '+str(message[index][0])
        os.system(ur)
    def usr_sign_quit():
        global flag
        flag=0
        window.destroy()

    def search(text_widget, keyword,tag):
        pos = '1.0'
        while True:
            idx = text_widget.search(keyword, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(keyword))
            text_widget.tag_add(tag, idx, pos)

    window=Tk()
    window.title('百度新闻搜索引擎')
    image2 = Image.open(r'0.jpg')
    image2=image2.resize((1000, 660))
    background_image = ImageTk.PhotoImage(image2)
    w = background_image.width()
    h = background_image.height()
    window.geometry('%dx%d+0+0' % (w, h))
    #背景图设置
    background_label = Label(window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (w, h, (screenwidth - w) / 2, (screenheight - h) / 2)
    window.geometry(alignstr)
    pcr = Image.open(r'title.png')
    pcr = pcr.resize((200, 67))
    pcr = ImageTk.PhotoImage(pcr)
    mek = tkinter.Label(window, image=pcr)
    mek.place(x=400,y=0)
    tk.Label(window,text='搜索条目==》', bg='blue',fg='white').place(x=85,y=70,width=100,height=30)
    #搜索栏
    var_usr_name=tk.StringVar()
    entry_1=tk.Entry(window,textvariable=var_usr_name)
    entry_1.insert(10,serach_text)
    entry_1.place(x=185,y=70,width=663,height=30)
    entry_1.bind('<Return>',serach)
    btngo = tkinter.Button(window,bg='blue', text='<搜索一下>',fg='white')
    btngo.place(x=847, y=70, width=70, height=30)
    btngo.bind("<Button-1>",serach)
    window.protocol('WM_DELETE_WINDOW', usr_sign_quit)
    #检索结果显示
    for i in range(6):
        index = leave*6 + i
        if(index>=page_len):
            break
        #标题
        xt1=tk.Text(window,bg='white',fg="brown")
        xt1.insert(END,'【'+str(index+1)+'】'+message[index][1])
        xt1.tag_config('tag',  foreground='red')
        for x in keywords:
            search(xt1, x,'tag')
        xt1.place(x=85,y=100+i*80,width=500,height=20)
        xt1.bind("<Double-Button-1>", lambda event, index=index: open_this(event, index))
        tk.Label(window, text=message[index][3],fg="green",anchor='w',bg='white').place(x=585, y=100 + i * 80, width=50, height=20)
        #摘要
        xt2=tk.Text(window,bg='white')
        xt2.insert(END,message[index][2])
        xt2.tag_config('tag',  foreground='red')
        for x in keywords:
            search(xt2, x,'tag')
        xt2.bind("<Double-Button-1>", lambda event, index=index: open_this(event, index))
        xt2.place(x=85, y=120 + i * 80, width=800, height=20)
        #链接
        xt=tk.Label(window, text=message[index][0],fg="blue",anchor='w',bg='white')
        xt.place(x=85, y=140 + i * 80, width=800, height=20)
        xt.bind("<Double-Button-1>", lambda event, index=index: open_this(event,index))
        #翻页按钮
    if(page_len!=0):
        tk.Label(window,text=str(leave+1)+'/'+str(end)).place(x=450,y=600,width=100,height=30)
        if(leave==0):
            bt1=tk.Button(window,text='下一页')
            bt1.place(x=560,y=600,width=80,height=30)
            bt1.bind('<Button-1>',next_page)
            bt2=tk.Button(window, text='尾页')
            bt2.place(x=640, y=600, width=80, height=30)
            bt2.bind('<Button-1>',last_page)
        elif(leave==end):
            bt1=tk.Button(window,text='首页')
            bt1.place(x=560,y=600,width=80,height=30)
            bt1.bind('<Button-1>',first_page)
            bt2=tk.Button(window, text='上一页')
            bt2.place(x=640, y=600, width=80, height=30)
            bt2.bind('<Button-1>',hea_page)
        else:
            bt1=tk.Button(window,text='首页')
            bt1.place(x=560,y=600,width=80,height=30)
            bt1.bind('<Button-1>',first_page)
            bt2=tk.Button(window, text='上一页')
            bt2.place(x=640, y=600, width=80, height=30)
            bt2.bind('<Button-1>',hea_page)
            bt3=tk.Button(window,text='下一页')
            bt3.place(x=720,y=600,width=80,height=30)
            bt3.bind('<Button-1>',next_page)
            bt4=tk.Button(window, text='尾页')
            bt4.place(x=800, y=600, width=80, height=30)
            bt4.bind('<Button-1>',last_page)
    # 主循环
    window.mainloop()
while(1):
    if(flag==0):
        break
    main_te_634(key)