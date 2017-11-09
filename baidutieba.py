#!/user/bin/env python
#coding=utf-8
import requests
import re
from requests.exceptions import ReadTimeout, ConnectionError, RequestException

class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceID = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    replaceExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceID,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.replaceExtraTag,"",x)
        return x.strip()

class BBB:
    def __init__(self, baseUrl, seeLZ, floorTag):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u"baidutieba"
        self.floorTag = floorTag

    def getPage(self,pageNum):
        try:
            url = self.baseURL+ self.seeLZ+ '&pn='+ str(pageNum)
            proxy = {"http": "http://135.252.192.168:5865"}
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
            response = requests.get(url, headers=headers, proxies=proxy)
            #html = response.text.decode("utf-8")
            return response.text.encode("utf-8")
        except ReadTimeout:
            print ('Timeout')
        except ConnectionError:
            print('ConnectionError')
        except RequestException:
            print('Error')
    def getTitle(self,page):
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None
    def getPageNum(self,page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None
    def getContent(self,page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            content = "\n"+self.tool.replace(item)+"\n"
            contents.append(content)
        return contents
    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")
    def writeData(self,contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + u"--------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1
    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "URL is unavailable, Please try it again!"
            return
        try:
            print "There are total " + str(pageNum) + " pages"
            for i in range(1,int(pageNum)+1):
                print "Writing the " + str(i) + " page's data"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError,e:
            print "Write error, reason is" + e.message
        finally:
            print "Done!"

print u"Please input the id"
baseURL = 'https://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("Whether only get LZ's words, yes 1, no 0 \n")
floorTag = raw_input("Whether write floor info, yes 1, no 0 \n")
bbb = BBB(baseURL,seeLZ,floorTag)
bbb.start()


