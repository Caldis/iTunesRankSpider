# -*- coding:utf-8 -*-

import re
import os
import urllib

class tools:
    #去除img标签,1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    #将多行空行删除
    removeNoneLine = re.compile('\n+')

    def __init__(self):
        pass

    #清除多余字符
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeNoneLine,"\n",x)
        #strip()将前后多余内容删除
        return x.strip()

    #保存图片
    def saveImgs(self,imagesURLs,imagesNames,name):
        number = 0
        for imageURL in imagesURLs:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            fileName = name + "/" + str(imagesNames[number]) + "." + fTail
            self.saveImg(imageURL,fileName)
            number += 1

    def saveImg(self,imageURL,fileName):
         u = urllib.urlopen(imageURL)
         data = u.read()
         f = open(fileName, 'wb')
         f.write(data)
         print u"正在保存图片到",fileName
         f.close()

    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"创建了名为",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经存在，无需创建'
            return False