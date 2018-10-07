'''
data : 2018.10.07
author : 极简XksA
goal : 可视化分析获取到的数据
'''
import csv

time = []
nickName = []
gender = []
cityName = []
userLevel = []
score = []
content = ''

# 读数据
def read_csv():
	content = ''
	# 读取文件内容
	with open(r'G:\maoyan\maoyan.csv', 'r', encoding='utf_8_sig', newline='') as file_test:
		# 读文件
		reader = csv.reader(file_test)
		i = 0
		for row in reader:
			if i != 0:
				time.append(row[0])
				nickName.append(row[1])
				gender.append(row[2])
				cityName.append(row[3])
				userLevel.append(row[4])
				score.append(row[5])
				content = content + row[6]
				# print(row)
			i = i + 1
		print('一共有：' + str(i - 1) + '个')
		return content

import re, jieba
#词云生成工具
from wordcloud import WordCloud,ImageColorGenerator
#需要对中文进行处理
import matplotlib.font_manager as fm
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from os import path

d=path.dirname(__file__)

stopwords_path = d + '/static/stopwords.txt'
# 评论词云分析
def word_cloud(content):
	import jieba, re, numpy
	from pyecharts import WordCloud
	import pandas as pd

	# 去除所有评论里多余的字符
	content = content.replace(" ", ",")
	content = content.replace(" ", "、")
	content = re.sub('[,，。. \r\n]', '', content)
		
	segment = jieba.lcut(content)
	words_df = pd.DataFrame({'segment': segment})
	# quoting=3 表示stopwords.txt里的内容全部不引用
	stopwords = pd.read_csv(stopwords_path, index_col=False, quoting=3, sep="\t", names=['stopword'],
		                        encoding='utf-8')
	words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
	words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
	words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
	test = words_stat.head(500).values
	codes = [test[i][0] for i in range(0, len(test))]
	counts = [test[i][1] for i in range(0, len(test))]
	wordcloud = WordCloud(width=1300, height=620)
	wordcloud.add("影评词云", codes, counts, word_size_range=[20, 100])
	wordcloud.render("H:\PyCoding\spider_maoyan\picture\c_wordcloud.html")

#定义个函数式用于分词
def jiebaclearText(text):
    #定义一个空的列表，将去除的停用词的分词保存
    mywordList=[]
    text = re.sub('[,，。. \r\n]', '', text)
    #进行分词
    seg_list=jieba.cut(text,cut_all=False)
    #将一个generator的内容用/连接
    listStr='/'.join(seg_list)
    listStr = listStr.replace("class","")
    listStr = listStr.replace("span", "")
    listStr = listStr.replace("悲伤逆流成河", "")
    #打开停用词表
    f_stop=open(stopwords_path,encoding="utf8")
    #读取
    try:
        f_stop_text=f_stop.read()
    finally:
        f_stop.close()#关闭资源
    #将停用词格式化，用\n分开，返回一个列表
    f_stop_seg_list=f_stop_text.split("\n")
    #对默认模式分词的进行遍历，去除停用词
    for myword in listStr.split('/'):
        #去除停用词
        if not(myword.split()) in f_stop_seg_list and len(myword.strip())>1:
            mywordList.append(myword)
    return ' '.join(mywordList)

# 生成词云图
def make_wordcloud(text1):
	text1 = text1.replace("悲伤逆流成河", "")
	bg = plt.imread(d + r"/static/znn1.jpg")
	# 生成
	wc = WordCloud(# FFFAE3
		background_color="white",  # 设置背景为白色，默认为黑色
		width=890,  # 设置图片的宽度
		height=600,  # 设置图片的高度
		mask=bg,
		# margin=10,  # 设置图片的边缘
		max_font_size=150,  # 显示的最大的字体大小
		random_state=50,  # 为每个单词返回一个PIL颜色
		font_path=d+'/static/simkai.ttf'  # 中文处理，用系统自带的字体
	).generate_from_text(text1)
	# 为图片设置字体
	my_font = fm.FontProperties(fname=d+'/static/simkai.ttf')
	# 图片背景
	bg_color = ImageColorGenerator(bg)
	# 开始画图
	plt.imshow(wc.recolor(color_func=bg_color))
	# 为云图去掉坐标轴
	plt.axis("off")
	# 画云图，显示
	# 保存云图
	wc.to_file(d+r"/picture/word_cloud.png")


# 评论者性别分布可视化
def sex_distribution(gender):
	# print(gender)
	from pyecharts import Pie
	list_num = []
	list_num.append(gender.count('0')) # 未知
	list_num.append(gender.count('1')) # 男
	list_num.append(gender.count('2')) # 女
	attr = ["其他","男","女"]
	pie = Pie("性别饼图")
	pie.add("", attr, list_num, is_label_show=True)
	pie.render("H:\PyCoding\spider_maoyan\picture\sex_pie.html")

# 评论者所在城市分布可视化
def city_distribution(cityName):
	city_list = list(set(cityName))
	city_dict = {city_list[i]:0 for i in range(len(city_list))}
	for i in range(len(city_list)):
		city_dict[city_list[i]] = cityName.count(city_list[i])
	# 根据数量(字典的键值)排序
	sort_dict = sorted(city_dict.items(), key=lambda d: d[1], reverse=True)
	city_name = []
	city_num = []
	for i in range(len(sort_dict)):
		city_name.append(sort_dict[i][0])
		city_num.append(sort_dict[i][1])
	
	import random
	from pyecharts import Bar
	bar = Bar("评论者城市分布")
	bar.add("", city_name, city_num, is_label_show=True, is_datazoom_show=True)
	bar.render("H:\PyCoding\spider_maoyan\picture\city_bar.html")
	
# 每日评论总数可视化分析
def time_num_visualization(time):
	from pyecharts import Line
	time_list = list(set(time))
	time_dict = {time_list[i]: 0 for i in range(len(time_list))}
	time_num = []
	for i in range(len(time_list)):
		time_dict[time_list[i]] = time.count(time_list[i])
	# 根据数量(字典的键值)排序
	sort_dict = sorted(time_dict.items(), key=lambda d: d[0], reverse=False)
	time_name = []
	time_num = []
	print(sort_dict)
	for i in range(len(sort_dict)):
		time_name.append(sort_dict[i][0])
		time_num.append(sort_dict[i][1])
			
	line = Line("评论数量日期折线图")
	line.add(
		"日期-评论数",
		time_name,
		time_num,
		is_fill=True,
		area_color="#000",
		area_opacity=0.3,
		is_smooth=True,
	)
	line.render("H:\PyCoding\spider_maoyan\picture\c_num_line.html")
	
# 评论者猫眼等级、评分可视化
def level_score_visualization(userLevel,score):
	from pyecharts import Pie
	userLevel_list = list(set(userLevel))
	userLevel_num = []
	for i in range(len(userLevel_list)):
		userLevel_num.append(userLevel.count(userLevel_list[i]))
	
	score_list = list(set(score))
	score_num = []
	for i in range(len(score_list)):
		score_num.append(score.count(score_list[i]))
		
	pie01 = Pie("等级环状饼图", title_pos='center', width=900)
	pie01.add(
		"等级",
		userLevel_list,
		userLevel_num,
		radius=[40, 75],
		label_text_color=None,
		is_label_show=True,
		legend_orient="vertical",
		legend_pos="left",
	)
	pie01.render("H:\PyCoding\spider_maoyan\picture\level_pie.html")
	pie02 = Pie("评分玫瑰饼图", title_pos='center', width=900)
	pie02.add(
		"评分",
		score_list,
		score_num,
		center=[50, 50],
		is_random=True,
		radius=[30, 75],
		rosetype="area",
		is_legend_show=False,
		is_label_show=True,
	)
	pie02.render("H:\PyCoding\spider_maoyan\picture\score_pie.html")

time = []
nickName = []
gender = []
cityName = []
userLevel = []
score = []
content = ''
content = read_csv()
# 1 词云
jiebaclearText(content)
make_wordcloud(content)
# pyecharts词云
# word_cloud(content)
# 2 性别分布
sex_distribution(gender)
# 3 城市分布
city_distribution(cityName)
# 4 评论数
time_num_visualization(time)
# 5 等级，评分
level_score_visualization(userLevel,score)

