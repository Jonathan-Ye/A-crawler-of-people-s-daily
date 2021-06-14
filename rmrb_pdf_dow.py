# 人民日报PDF下载
# 支持2020年7月1日起新版，并兼容旧版
# 2021.6.13

import os
import datetime
import requests
from bs4 import BeautifulSoup


def generateDate(userInputStart, userInputEnd):
    try:
        start = datetime.datetime.strptime(userInputStart,"%Y%m%d")
        end = datetime.datetime.strptime(userInputEnd,"%Y%m%d")
        step = datetime.timedelta(days=1)
        timeList = []
        while start <= end:
            timeList.append(start)
            start += step
        return timeList
    except:
        print("时间处理异常")
        exit()

def getHTML(date):
    kv = {'user-agent': 'Mozilla/5.0'}      # 重定义用户标识
    # 获取人民日报首页url
    url = "http://paper.people.com.cn/rmrb/html/"+date[:4]+"-"+date[4:6]+"/"+date[6:]+"/nbs.D110000renmrb_01.htm"

    try:
        r = requests.get(url, timeout=10, headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text, url
    except:
        print("获取HTML网页产生异常")
        exit()


def parsePage(html, flag):
    try:
        #分析旧版首页
        if flag == 0:
            soup = BeautifulSoup(html, "html.parser")
            rightPDF = soup.find_all(class_= "right_title-pdf")  # 查找right_title-pdf类标签
            pdfNum = len(rightPDF)
            suburl = rightPDF[0].a.attrs['href']    # ../../../page/2020-02/01/01/rmrb2020020101.pdf
            suburl = suburl[9:]                     # page/2020-02/01/01/rmrb2020020101.pdf

        #分析新版首页
        elif flag ==1:
            soup = BeautifulSoup(html, "html.parser")
            rightPDF = soup.find_all(class_= "right btn")  # 查找right btn类标签
            title = soup.find_all(class_ = "swiper-slide")  # 查找swiper-slide类标签
            pdfNum = len(title)                 # 因为每页只有一个链接，通过title获取版数

            suburl = rightPDF[0].a.attrs['href']    # ../../../images/2020-07/01/01/rmrb2020070101.pdf
            suburl = suburl[9:]                     # images/2020-07/01/01/rmrb2020070101.pdf


    except:
        print("分析页面产生异常")
        exit()

    # 生成具体pdfUrl
    pdfUrl = "http://paper.people.com.cn/rmrb/" + suburl
    return pdfUrl, pdfNum

def savePDF(pdfUrl, pdfNum):
    for i in range(1,pdfNum+1):
        pdfUrlPage = pdfUrl[:-21] + "%02d"%i + pdfUrl[-19:-6] + "%02d"%i + pdfUrl[-4:]  #修改url页面中的版数
        print(pdfUrlPage,end = '\t')
        t = requests.get(pdfUrlPage)    # 向网站请求
        print("下载中...", end = '\t')

        # 保存至本地（创建以日期为文件名的文件夹）
        if os.path.exists("./PDF_Download/" + pdfUrlPage[-14:-6]) == False:     #检查以日期命名文件夹是否存在
            os.mkdir("./PDF_Download/" + pdfUrlPage[-14:-6])

        with open("./PDF_Download/" + pdfUrlPage[-14:-6] +"/" + pdfUrlPage[-14:],'wb') as f:
            f.write(t.content)
            f.close()

        print("pdf下载成功")


if __name__ == "__main__" :
    print("{:^40}".format("人民日报PDF下载工具"))
    print("{:=^40}".format(""))
    print("{:<40}".format("支持2020年7月1日起新版，并兼容旧版"))
    print("{:<40}".format("开发日期：2021.06.14"))
    print("{:<40}".format("版本：v1.0"))
    print("{:=^40}".format(""))

    try:
        userInputStart = input("请输入开始时间，如“20210101”：")
        userInputEnd = input("请输入结束时间，如“20210701”：")
    except:
        print("时间输入异常")
    timeList = []
    timeList = generateDate(str(userInputStart),str(userInputEnd))
    for date in timeList:
        dateStr = date.strftime("%Y%m%d")
        html, url = getHTML(dateStr)

        # 比较日期与2020年7月1日大小， 之前返回0， 之后返回1
        if date < datetime.datetime.strptime("20200701","%Y%m%d"):
            flag = 0
        else:
            flag = 1

        print("日期：{}".format(dateStr))
        pdfUrl, pdfNum = parsePage(html, flag)

        if os.path.exists("PDF_Download") == False:     #检查PDF总文件夹是否存在
            os.mkdir("PDF_Download")
        savePDF(pdfUrl, pdfNum)

    os.system("pause")