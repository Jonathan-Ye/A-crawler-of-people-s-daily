# 人民日报官网文本爬取
# 适用于2020年7月1日起新版
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
        timelist = []
        while start <= end:
            timelist.append(start)
            start += step
        return timelist
    except:
        print("时间处理异常")
        exit()




def getHTML(date):
    kv = {'user-agent': 'Mozilla/5.0'}      # 重定义用户标识

    # 获取人民日报首页头版头条详情页url
    url = "http://paper.people.com.cn/rmrb/html/" + date[:4] + "-" + date[4:6] + "/" + date[6:] + \
          "/nw.D110000renmrb_" + date + "_1-01.htm"

    try:
        r = requests.get(url, timeout=10, headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text, url
    except:
        print("获取HTML网页产生异常")
        exit()




def parsePage(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        #rightText = soup.find_all(id = "ozoom")
        rightText = soup.select("#ozoom p")

        text = ""
        for i in rightText:
            text = text + i.string

    except:
        print("分析页面产生异常")
        exit()
    return text

def saveText(date, text):
    with open("./TEXT_Download/" + "{}.txt".format(date), 'w', encoding='utf-8') as f:
        f.write(text)
        f.close()



def combineText():
    #判断文件是否存在
    if os.path.exists("./TEXT_Download/Combine_TEXT") == True:
        print("请删除Combine_TEXT再试！")
        exit()

    # 创建总文本文件
    with open("./TEXT_Download/Combine_TEXT.txt", 'a+', encoding='utf-8') as f:
        for i in os.walk("./TEXT_Download/"):
            for j in i[2]:
                if j == "Combine_TEXT":
                    continue
                print("正在合并：" + j)
                t = ""
                with open("./TEXT_Download/" + j, 'r', encoding='utf-8') as ff:     # 打开每一个子文件
                    t = ff.read()
                    f.write(t)
                    ff.close()                                                      # 子文件关闭

        f.close()       # 总文件关闭



if __name__ == "__main__":
    print("{:^40}".format("人民日报头条文本爬取工具"))
    print("{:=^40}".format(""))
    print("{:<40}".format("适用于2020年7月1日起新版"))
    print("{:<40}".format("开发日期：2021.06.14"))
    print("{:<40}".format("版本：v1.0"))
    print("{:=^40}".format(""))

    try:
        userInputStart = input("请输入开始时间，在20200701之后，如“20210101”：")
        userInputEnd = input("请输入结束时间，在20200701之后，如“20210701”：")
    except:
        print("时间输入异常")

    # 判断开始日期与2020年7月1日大小
    if datetime.datetime.strptime(userInputStart, "%Y%m%d") < datetime.datetime.strptime("20200701", "%Y%m%d"):
        print("时间输入错误，程序退出！")
        exit()

    timeList = []
    timeList = generateDate(str(userInputStart),str(userInputEnd))
    for date in timeList:
        dateStr = date.strftime("%Y%m%d")
        print("日期：{}".format(dateStr), end='\t')
        print("内容获取中...", end='\t')
        html, url = getHTML(dateStr)
        text = ""
        text = parsePage(html)

        if os.path.exists("TEXT_Download") == False:     #检查text总文件夹是否存在
            os.mkdir("TEXT_Download")
        saveText(dateStr, text)
        print("保存成功")

    print("总文本合并中...")
    combineText()
    print("全部完成！")

    os.system("pause")
