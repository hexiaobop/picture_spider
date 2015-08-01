# -*- coding: utf-8-*-
import urllib2
from bs4 import BeautifulSoup
import re
import threading
import urllib
import time
import Queue


class Get_picture:
    def __init__(self):
        self.number = 0;
        self.urlpage = 0
        self.url_list = Queue.Queue()
        self.numbername = 0;

    def get_bigpictur(self,url):

        response = urllib2.urlopen(url).read().decode("utf-8")

        result = re.findall('''<img id="img2" src="(.*?)">''',response,re.S)
        if(len(result)<1):
            print "没有多张"
            result = re.findall('''<div class="picture" id="imglist">.*?<img src="(.*?)".*?/>''',response,re.S)
        urllib.urlretrieve(result[0],"1-%s.jpg"%self.numbername)                                          # 下载大图片
        print result[0]

    def get_picture(self, url):                                   # 获取图片资源
        response = urllib2.urlopen(url).read().decode("utf-8")
        # result = re.findall('''<img src="(.*?)" ''',response)
        soup = BeautifulSoup(response)
        result = soup.find("div", {"class": "clearfix grid"})
        urlnumber = soup.find("div", {"id": "pager"})
        self.urlpage = int(urlnumber.b.string) / 12 + 1

        for i in result.contents:
            if (len(i) < 10):
                pass
            else:
                self.numbername=self.numbername+1
                self.number = self.number + 1
                href = "http://www.xianhua.sn.cn/"+i.contents[0].a['href']
                xiaotuur = i.contents[0].img["src"]

                name = i.b.string
                price =i.contents[0].img["alt"], i.b.string
                print i.contents[0].img["src"], i.contents[0].img["alt"], i.b.string,href
                self.get_bigpictur(href)
                # urllib.urlretrieve(ur,"%s.jpg"%self.numbername)                           #下载小图片

        print "------------------已经搞定" + str(self.number)

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
                time.sleep(1)
            for j in threads:
                j.join()
if __name__ == '__main__':
    first = Get_picture()
    first.get_all()
    print "----------------完成" + str(first.number) + "资源"
    print "程序结束！！！！！！！！！！！！！"


