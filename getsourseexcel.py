# -*- coding: utf-8-*-
import urllib2
from bs4 import BeautifulSoup
import re
import threading
import urllib
import time
import Queue
import xlrd
import xlwt
from xlutils.copy import copy
import thread

class Get_picture:
    def __init__(self,table):
        self.number = 0;
        self.urlpage = 0
        self.url_list = Queue.Queue()
        self.numbername = 0;
        self.totalresource=0
        self.lock = thread.allocate_lock()                                #线程锁，确保写入的连续数据是同一页内容
        self.table=table


    def save_excel(self,row,name,price,introduce):


        self.table.write(row,0,name)
        self.table.write(row,1,price)
        self.table.write(row,2,introduce)



    def get_bigpictur(self,url):

        response = urllib2.urlopen(url).read().decode("utf-8")

        result = re.findall('''<img id="img2" src="(.*?)">''',response,re.S)
        if(len(result)<1):
            print "没有多张"
            result = re.findall('''<div class="picture" id="imglist">.*?<img src="(.*?)".*?/>''',response,re.S)
        #urllib.urlretrieve(result[0],"1-%s.jpg"%self.numbername)                                          # 下载大图片
        print result[0]

    def get_picture(self, url):                                   # 获取图片资源
        response = urllib2.urlopen(url).read().decode("utf-8")
        # result = re.findall('''<img src="(.*?)" ''',response)
        soup = BeautifulSoup(response)
        result = soup.find("div", {"class": "clearfix grid"})
        urlnumber = soup.find("div", {"id": "pager"})
        self.totalresource = urlnumber
        self.urlpage = int(urlnumber.b.string) / 12 + 1
        self.lock.acquire()
        data = xlrd.open_workbook('second.xls')
        for i in result.contents:
            if (len(i) < 10):
                pass
            else:
                self.numbername=self.numbername+1
                self.number = self.number + 1
                href = "http://www.xianhua.sn.cn/"+i.contents[0].a['href']
                xiaotuur = i.contents[0].img["src"]
                introduce =i.contents[0].img["alt"],
                name = introduce[0][0:5]
                price = i.b.string
                price1 = int(price[1:-1])
                print i.contents[0].img["src"], i.contents[0].img["alt"], i.b.string,href,price1,name,

                self.save_excel((self.number-1),name,price1,introduce)


                self.get_bigpictur(href)
                # urllib.urlretrieve(ur,"%s.jpg"%self.numbername)                           #下载小图片

        print "------------------已经搞定" + str(self.number)
        self.lock.release()


    def get_urllist(self):  # 构造所有的页面链接
        url = "http://www.xianhua.sn.cn/products-15-0-0-0-0x0x0x0-9-salesnum-DESC.html"
        url1 = url.split("-9-")
        for i in range(2, self.urlpage + 1):
            url2 = url1[0] + "-" + str(i) + "-" + url1[1]
            self.url_list.put(url2)

    def get_all(self):
        url = "http://www.xianhua.sn.cn/products-15-0-0-0-0x0x0x0.html"
        self.get_picture(url)
        self.get_urllist()

        print "-----------------共有" + str(self.urlpage) + "页需要抓取"
        while (self.url_list.qsize() > 0):
            threads = []
            for i in range(1, 3):

                url1 = self.url_list.get()
                print "线程开始-----------取得的"+url1
                t = threading.Thread(target=self.get_picture, args=( url1, ))
                threads.append(t)
                t.start()
                time.sleep(2)
            for j in threads:
                j.join()
if __name__ == '__main__':
    data = xlwt.Workbook()
    table = data.add_sheet('message')
    first = Get_picture(table)




    first.get_all()
    data.save('second.xls')
    print "----------------完成" + str(first.number) + "资源"
    print "程序结束！！！！！！！！！！！！！"


