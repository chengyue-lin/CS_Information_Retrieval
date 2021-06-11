#encoding=utf-8
from bs4 import BeautifulSoup
from queue import Queue
import socket
import urllib.request as request
import zlib
import re
import json
import threadpool
import threading

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head',
	'input',
	'script',
	'style'
]


class linkQuence:
    def __init__(self):
        #Collection of visited URLs
        self.visted=[]
        #Collection of URLs to be accessed
        self.unVisited=[]
    #Get the visited URL queue
    def getVisitedUrl(self):
        return self.visted
    #Gets the unreached URL queue
    def getUnvisitedUrl(self):
        return self.unVisited
    #Add to the visited URL queue
    def addVisitedUrl(self,url):
        self.visted.append(url)
    #Remove visited URL
    def removeVisitedUrl(self,url):
        self.visted.remove(url)
    #Unreached URL out of the queue
    def unVisitedUrlDeQuence(self):
        try:
            return self.unVisited.pop()
        except:
            return None
    #Ensure that each URL is accessed only once
    def addUnvisitedUrl(self,url):
        if url!="" and url not in self.visted and url not in self.unVisited:
            self.unVisited.insert(0,url)
    #Get the number of URLs visited
    def getVisitedUrlCount(self):
        return len(self.visted)
    #Get the number of URLs not visited
    def getUnvistedUrlCount(self):
        return len(self.unVisited)
        #Determine whether the unreached URL queue is empty
    def unVisitedUrlsEnmpy(self):
        return len(self.unVisited)==0


def wirteData(dataQueue):
    stop=True
    with open("data.json","w",encoding="utf-8") as fw:
        while stop:
            if not dataQueue.empty():
                text=dataQueue.get()
                if text=='@@@queueStop@@@':
                    stop=False
                else:
                    fw.write(text)
                    fw.write("\n")
            else:
                pass
def saveData(dataQueue,url,text):
    dictsd={}
    dictsd['url']=url
    dictsd['text']=text
    dataQueue.put(json.dumps(dictsd))


class MyCrawler:
    def __init__(self,seeds):
            #Initialize URL queue with seed
            self.linkQuence=linkQuence()
            if isinstance(seeds,str):
                self.linkQuence.addUnvisitedUrl(seeds)
            if isinstance(seeds,list):
                for i in seeds:
                    self.linkQuence.addUnvisitedUrl(i)
            print("Add the seeds url \"%s\" to the unvisited url list"%str(self.linkQuence.unVisited))


    def crawling(self,seeds,crawl_count,dataqueue):
            while self.linkQuence.unVisitedUrlsEnmpy() is False and self.linkQuence.getVisitedUrlCount()<=crawl_count:

                visitUrl=self.linkQuence.unVisitedUrlDeQuence()
                print("Pop out one url \"%s\" from unvisited url list"%visitUrl)
                if visitUrl is None or visitUrl=="":
                    continue
                #Get hyperlinks
                links=self.getHyperLinks(visitUrl,dataqueue)
                #links=getHyperLinks(visitUrl)

                print("Get %d new links"%len(links))
                #Put the URL into the URL that has been accessed
                self.linkQuence.addVisitedUrl(visitUrl)
                print("Visited url count: "+str(self.linkQuence.getVisitedUrlCount()))
                #未访问的url入列
                for link in links:
                    self.linkQuence.addUnvisitedUrl(link)
                print("%d unvisited links:"%len(self.linkQuence.getUnvisitedUrl()))


    #The unreached URL is listed
    def getHyperLinks(self,url,dataQueue):
        links=[]
        data=self.getPageSource(url)
        if data[0]=="200":
            soup=BeautifulSoup(data[1])
            a=soup.findAll("a",{"href":re.compile(".*")})
            for i in a:
                if i["href"].find("http://")!=-1:
                    links.append(i["href"])
            text=''
            original_text=soup.findAll(text=True)
            for t in original_text:
                if t.parent.name not in blacklist:
                    text += '{} '.format(t)
            saveData(dataQueue,url,  text)
        return links

        #Access to web source code
    def getPageSource(self,url,timeout=20,coding=None):
        try:
            #socket.settime(100)
            socket.setdefaulttimeout(timeout)

            #req = urllib.request(url)
            req = request.Request(url)

            req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')

            response = request.urlopen(req)
            #if coding is None:
                #coding= response.headers.getparam("charset")
            if coding is None:
                page=response.read()
            else:
                page=response.read()
                page=page.decode(coding).encode('utf-8')
            return ["200",page]
        except Exception as e:
            print(str(e))
            return [str(e),None]



def main(seeds,crawl_count):
        poolLen=8
        dataQueue = Queue()
        t = threading.Thread(target=wirteData, args=(dataQueue,))
        t.start()
        pool = threadpool.ThreadPool(poolLen)
        param = []
        craw = MyCrawler(seeds)
        for i in range(0, poolLen):
            a = ([seeds, crawl_count, dataQueue], None)
            param.append(a)
        tasks = threadpool.makeRequests(craw.crawling, param)
        [pool.putRequest(task) for task in tasks]
        pool.wait()
        dataQueue.put("@@@queueStop@@@")
        print("over")
if __name__=="__main__":
        main(["http://www.stanford.edu"],50)