# -*- coding:utf-8 -*-

from urllib import quote
import urllib2
import re
import json


#抓取图片
class topSongsSpider:

    #页面初始化
    def __init__(self):
        self.siteURL = "https://itunes.apple.com/jp/rss/topsongs/limit=100/xml"
        self.mainPage = ""
        self.updateTime = ""
        self.songIDs = []
        self.albumURLs = []
        self.artistURLs = []
        self.cover55URLs = []
        self.cover60URLs = []
        self.cover170URLs = []
        self.albumNames = []
        self.artistNames = []
        self.singleNames = []

#初始化信息
    #初始化主页面
    def initMainPage(self):
        try:
            print u"正在初始化主页面"
            url = self.siteURL
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            self.mainPage = response.read()
            return response
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接失败,错误原因:",e.reason
                return None

    #初始化歌曲ID
    def initSongsID(self):
        if len(self.mainPage):
            print u"正在初始化歌曲ID"
            pattern = re.compile('<id im:id="(.*?)">',re.S)
            self.songIDs = re.findall(pattern,self.mainPage)
        else:
            print u"页面未初始化，SongID生成失败"


#获取信息-URL
    #获取更新时间
    def getUpdateTime(self):
        if len(self.mainPage):
             #print u"正在获取更新时间  2015-06-07T06:27:35-07:00  "
            pattern = re.compile('</title><updated>(.*?)T(.*?)-.*?</updated><link',re.S)
            self.updateTime = re.findall(pattern,self.mainPage)
            return self.updateTime
        else:
            print u"页面未初始化，更新时间获取失败"

    #获取Album页面的URL表
    def getAlbumURLs(self):
        if len(self.mainPage):
            #print u"正在获取Album页面的URL"
            pattern = re.compile('<id im:id=".*?">(.*?)\?i=',re.S)
            self.albumURLs = re.findall(pattern,self.mainPage)
            return self.albumURLs
        else:
            print u"页面未初始化，AlbumURL获取失败"

    #获取Artist页面的URL表
    def getArtistURLs(self):
        if len(self.mainPage):
            #print u"正在获取Artist页面的URL"
            pattern = re.compile('<im:artist href="(.*?)\?uo=',re.S)
            self.artistURLs = re.findall(pattern,self.mainPage)
            return self.artistURLs
        else:
            print u"页面未初始化，ArtistURL获取失败"

    #获取Cover55的URL表
    def getCover55URLs(self):
        if len(self.mainPage):
            #print u"正在获取Cover55x55的URL"
            pattern = re.compile('<im:image height="55">(.*?)</im:image>',re.S)
            self.cover55URLs = re.findall(pattern,self.mainPage)
            return self.cover55URLs
        else:
            print u"页面未初始化，CoverURL获取失败"

    #获取Cover60的URL表
    def getCover60URLs(self):
        if len(self.mainPage):
            #print u"正在获取Cover60x60的URL"
            pattern = re.compile('<im:image height="60">(.*?)</im:image>',re.S)
            self.cover60URLs = re.findall(pattern,self.mainPage)
            return self.cover60URLs
        else:
            print u"页面未初始化，CoverURL获取失败"

    #获取Cover170的URL表
    def getCover170URLs(self):
        if len(self.mainPage):
            #print u"正在获取Cover170x170的URL"
            pattern = re.compile('<im:image height="170">(.*?)</im:image>',re.S)
            self.cover170URLs = re.findall(pattern,self.mainPage)
            return self.cover170URLs
        else:
            print u"页面未初始化，CoverURL获取失败"

    #获取自定义的专辑封面URL表
    def getCustomCoverURLs(self,country,entity,limit,term,rex=1500,quality=100):
        try:
            #print "正在查询服务器,搜索内容:[国家:%s，类型:%s，上限:%s 关键字:%s]" %(country,entity,str(limit),str(term))
            encoded = quote(term)
            url = "https://itunes.apple.com/search?country="+country+"&entity="+entity+"&limit="+str(limit)+"&term="+encoded
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            results = json.loads(response.read())
            url = results['results'][0]['artworkUrl100']
            imgURL = re.match(re.compile('http://.*?\..*?\..*?\.'),url)
            return imgURL.group()+str(rex)+'x'+str(rex)+'-'+str(quality)+'.jpg'
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"获取失败,错误原因:",e.reason
                return None

    #获取Album名称表
    def getAlbumNames(self):
        if len(self.mainPage):
            #print u"正在获取Album名称"
            pattern = re.compile('<im:collection><im:name>(.*?)</im:name>',re.S)
            self.albumNames = re.findall(pattern,self.mainPage)
            return self.albumNames
        else:
            print u"页面未初始化，AlbumName获取失败"

    #获取Artist名称表
    def getArtistNames(self):
        if len(self.mainPage):
            #print u"正在获取Artist名称"
            pattern = re.compile('<im:artist href=".*?">(.*?)</im:artist>',re.S)
            self.artistNames = re.findall(pattern,self.mainPage)
            return self.artistNames
        else:
            print u"页面未初始化，ArtistName获取失败"

    #获取Single名称表
    def getSingleNames(self):
        if len(self.mainPage):
            #print u"正在获取Single名称"
            pattern = re.compile('<id im:id=".*?<title>(.*?) - ',re.S)
            self.singleNames = re.findall(pattern,self.mainPage)
            return self.singleNames
        else:
            print u"页面未初始化，SingleName获取失败"

    #Test
    def test(self):
        self.initMainPage()
        self.initSongsID()
        self.getUpdateTime()
        print u"更新时间 :", self.updateTime[0][0], self.updateTime[0][1]
        for num in range(0,99):
            print u"名次    :",num+1
            print u"歌曲名称 :", self.getSingleNames()[num]
            print u"歌手名称 :", self.getArtistNames()[num]
            s = self.getAlbumNames()[num]
            print u"专辑名称 :", s
            print u"歌曲ID  :", self.songIDs[num]
            print u"歌手URL :", self.getArtistURLs()[num]
            print u"专辑URL :",self.getAlbumURLs()[num]
            print u"专辑封面URL:",self.getCover170URLs()[num]
            print u"自定专辑封面Url:",self.getCustomCoverURLs("jp","album",'1',s,'1000','100')


spider = topSongsSpider()
spider.test()