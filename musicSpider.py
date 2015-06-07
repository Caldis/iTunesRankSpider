# -*- coding:utf-8 -*-

import json
import requests
import hashlib
import random

default_timeout = 20

class musicSpider:
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }
        self.cookies = {
            'appver': '1.5.2'
        }

    #加密算法, 基于https://github.com/yanunon/NeteaseCloudMusic实现
    def encrypted_id(self,dfsID):
        magic = bytearray('3go8&$8*3*3h0k(2)2')
        song_id = bytearray(dfsID)
        magic_len = len(magic)
        for i in xrange(len(song_id)):
            song_id[i] = song_id[i]^magic[i%magic_len]
        m = hashlib.md5(str(song_id))
        result = m.digest().encode('base64')[:-1]
        result = result.replace('/', '_')
        result = result.replace('+', '-')
        return result

    #生成httpRequest
    def httpRequest(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):
        connection = json.loads(self.rawHttpRequest(method, action, query, urlencoded, callback, timeout))
        return connection
    def rawHttpRequest(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):
        if (method == 'GET'):
            url = action if (query == None) else (action + '?' + query)
            connection = requests.get(url, headers=self.header, timeout=default_timeout)
            return connection.text
        elif (method == 'POST'):
            connection = requests.post(action,data=query,headers=self.header,timeout=default_timeout)
            connection.encoding = "UTF-8"
            return connection.text

    #搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
    def search(self, keyWord, stype=1, offset=0, total='true', limit=1):
        action = 'http://music.163.com/api/search/get'
        data = {
            's': keyWord,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        result =  self.httpRequest('POST', action, data)
        return result

    #从搜索result获取songID
    def getSongID(self,searchResult):
        if searchResult['result']['songCount'] != 0:
            return searchResult['result']['songs'][0]['id']
        else:
            return None

    #用songID获取songDetail
    def getSongDetail(self,songID):
        action = "http://music.163.com/api/song/detail/?id=" + str(songID) + "&ids=[" + str(songID) + "]"
        try:
            detail = self.httpRequest('GET', action)
            return detail
        except:
            return []

    #从songDetail获取dfsID
    def getDfsID(self,detail):
        hdfsID = detail['songs'][0]['hMusic']['dfsId']
        mdfsID = detail['songs'][0]['mMusic']['dfsId']
        ldfsID = detail['songs'][0]['lMusic']['dfsId']
        return hdfsID,mdfsID,ldfsID

    #获取songURL
    def getSongURL(self,dfsID):
        enc_id =  self.encrypted_id(str(dfsID))
        url = "http://m%s.music.126.net/%s/%s.mp3"%(random.randrange(1,3), enc_id, str(dfsID))
        return url

    #直接搜索得出URL，Quality：0=high，1=mid，2=low，Fuzzy：0=off，1=on
    def spiderUrl(self, songName, artist, quality=0, fuzzy=1):
        keyWord = str(songName),str(artist)
        result = self.search(keyWord)
        songID = self.getSongID(result)
        if songID is None:
            if fuzzy:
                print u"无法搜索到指定曲目，尝试模糊搜索..."
                result = self.search(str(songName))
                songID = self.getSongID(result)
                if songID is None:
                    print u"模糊搜索失败，无指定曲目"
                else:
                    print u"模糊搜索成功，歌手为:%s" %(result['result']['songs'][0]['artists'][0]['name'])
                    detail = self.getSongDetail(songID)
                    dfsID  = self.getDfsID(detail)
                    songURL = spider.getSongURL(dfsID[quality])
                    return songURL
            else:
                print u"无法搜索到指定曲目，退出搜索"
        else:
            detail = self.getSongDetail(songID)
            dfsID  = self.getDfsID(detail)
            songURL = spider.getSongURL(dfsID[quality])
            return songURL

    #Test
    def test(self):
        url = spider.spiderUrl("See You Again (feat. Charlie Puth)","ウィズ・カリファ")
        print u"URL:",url


spider = musicSpider()
spider.test()