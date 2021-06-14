import jieba
import wordcloud
import imageio        #导入需要的库

mk = imageio.imread("chinamap.png")     #放入模板
f0 = open('词表.txt',encoding='UTF-8')    #制作去词表
txt1 = f0.read()
f0.close()
txt1 = txt1.split()
txt1 += ["的",'在','会主','书记','总书记','和','月','日','等','是','从','年'
        ,'年','到','中央','主义','新','四五','国共','高质','了','现代','也','说']
txt1 = set(txt1)


w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttc',      #这个选项是字体
                        mask=mk,
                        scale=15,
                        stopwords=txt1)


f = open('Combine_TEXT.txt',encoding='utf-8')     #打开需要制作词云的文件
txt = f.read()
f.close()

txtlist = jieba.cut_for_search(txt)    #获取文本列表
string = " ".join(txtlist)

w.generate(string)        #绘制词云

w.to_file('rmrb3.png')           # 将词云图片导出到当前文件夹


