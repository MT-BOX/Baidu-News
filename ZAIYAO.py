from datetime import datetime
import math
import jieba

import re
class MyTfIdf_634:
    def __init__(self, s):  # 初始化参数，即得到待操作的文本
        self.s = s
    def getallchineseword_634(self, tx):  # 去停用词
        t = re.compile('[\u4e00-\u9fff]+').findall(tx)
        x = ''
        x = x.join(t)
        return x
    def jieba_fenc_634(self,tx): #jieba分词统计
        txt = self.getallchineseword_634(tx)
        words = jieba.lcut(txt,cut_all=False)  # 使用精确模式对文本进行分词
        end = datetime.now()
        counts = {}  # 通过键值对的形式存储词语及其出现的次数
        for word in words:
            counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1
        items = list(counts.items())  # 将键值对转换成列表
        return items

    def tf_634(self,data):#计算TF
        tf_word =[]
        for i in range(len(data)):
            doc=data[i]
            mix=0
            ts=[]
            for j in range(len(doc)):
                mix=mix+doc[j][1]
            for j in range(len(doc)):
                ts.append((doc[j][0],doc[j][1]/mix))
            tf_word.append(ts)
        return tf_word


    def get_worfdf_634(self,data):#获取IDF
        word2df=set()
        word2d=dict()
        list_1=[]
        for doc in data:#去除字频
            hr=[]
            for i in range(len(doc)):
                hr.append(doc[i][0])
            list_1.append(hr)
        for it in list_1:
            for doc in it:
                mix = 0
                for j in list_1:
                    if doc in j:
                        mix=mix+1
                word2df.add((doc,math.log(len(data)/mix)))#添加集合

        word2df=list(word2df)

        for i in range(len(word2df)):#列表转字典
            word2d[str(word2df[i][0])]=(word2df[i][1])
        return word2d

    def getTFIDF_634(sef,tfs,idf):
        tf_list=[]
        for i in range(len(tfs)):
            doc = tfs[i]
            ts=[]
            for j in range(len(doc)):
                ts.append((doc[j][0],doc[j][1]*idf[doc[j][0]]))
            tf_list.append(ts)
        return tf_list

    def getTFIDF_all_634(self):
        data = []
        for i in range(len(self.s)):
            da = self.jieba_fenc_634(self.s[i])
            data.append(da)
        tf_word = self.tf_634(data)  # 获取TF
        # print(tf_word)
        word2df = self.get_worfdf_634(data)  # 获取IDF
        # print(word2df)
        tf_list = self.getTFIDF_634(tf_word, word2df)  # 计算WT
        return tf_list
class zaiyao_634:
    def __init__(self,text, keywords,length):  # 初始化参数，即得到待操作的文本
        self.keywords = keywords
        self.text=text
        self.length=length
    def indexstr_634(self,str2):
        '''查找指定字符串str1包含指定子字符串str2的全部位置，
        以列表形式返回'''
        lenth2=len(str2)
        lenth1=len(self.text)
        indexstr2=[]
        i=0
        while str2 in self.text[i:]:
            indextmp = self.text.index(str2, i, lenth1)
            indexstr2.append(indextmp)
            i = (indextmp + lenth2)
        return indexstr2

    def findall_key_634(self):#查找到所有关键词位置
        locae = []
        for str2 in self.keywords:
            locae = locae + self.indexstr_634(str2)
        locae.sort()
        return locae

    def cut_key_634(self,loact):#将文档按指定窗口大小分割
        window=[]
        for i in loact:
            if(i+self.length<=len(self.text)):
                window.append(self.text[i:i+self.length])
            else:
                window.append(self.text[i:])
        return window

    def find_max_634(self,TFIDF):#计算并找到分值最大的窗口
        win_score=[]
        for i in range(len(TFIDF)):
            bs=TFIDF[i]
            bs_score=0
            for j in range(len(bs)):
                word=bs[j][0]
                score=bs[j][1]
                if(word in self.keywords):
                    bs_score=bs_score+score
            win_score.append(bs_score)
        return win_score.index(max(win_score))
    def getZAOYAO_634(self):
        locat = self.findall_key_634()
        windows = self.cut_key_634(locat)
        TFIDF = MyTfIdf_634(windows).getTFIDF_all_634()
        if(len(locat)>0):
            index = self.find_max_634(TFIDF)
            return [windows[index],len(locat)]
        else:
            return [str(self.keywords),0]