'''
data : 2018.10.06
author : 极简XksA
goal : 被反爬了，在这里修改数据继续往前爬取，保护main_page数据不被改动
'''

# 猫眼电影介绍url
# http://maoyan.com/films/1217236

import requests, time
from fake_useragent import UserAgent
import json, csv, os
import pandas as pd


class Spidermaoyan():
	headers = {
		"User-Agent": UserAgent(verify_ssl=False).random,
		"Host": "m.maoyan.com",
		"Referer": "http://m.maoyan.com/movie/1217236/comments?_v_=yes"
	}
	
	def __init__(self, url, time):
		self.url = url
		self.time = time
	
	# 发送get请求
	def get_json(self):
		# 发送get请求
		response_comment = requests.get(self.url, headers=self.headers)
		json_comment = response_comment.text
		json_comment = json.loads(json_comment)
		# print(json_comment)
		return json_comment
	
	# 获取数据并存储
	def get_data(self, json_comment):
		json_response = json_comment["cmts"]  # 列表
		print(len(json_response))
		list_info = []
		for data in json_response:
			cityName = data["cityName"]
			content = data["content"]
			if "gender" in data:
				gender = data["gender"]
			else:
				gender = 0
			nickName = data["nickName"]
			userLevel = data["userLevel"]
			score = data["score"]
			list_one = [self.time, nickName, gender, cityName, userLevel, score, content]
			list_info.append(list_one)
		self.file_do(list_info)
	
	# 存储文件
	def file_do(self, list_info):
		# 获取文件大小
		file_size = os.path.getsize(r'G:\maoyan\maoyan.csv')
		if file_size == 0:
			# 表头
			name = ['评论日期', '评论者昵称', '性别', '所在城市', '猫眼等级', '评分', '评论内容']
			# 建立DataFrame对象
			file_test = pd.DataFrame(columns=name, data=list_info)
			# 数据写入
			file_test.to_csv(r'G:\maoyan\maoyan.csv', encoding='utf_8_sig', index=False)
		else:
			with open(r'G:\maoyan\maoyan.csv', 'a+', encoding='utf_8_sig', newline='') as file_test:
				# 追加到文件后面
				writer = csv.writer(file_test)
				# 写入文件
				writer.writerows(list_info)


# 猫眼电影短评接口
offset = 900
# 电影是2018.9.21上映的
startTime = '2018-10-06'
day = [22, 23, 24, 25, 26, 27, 28, 29, 30, 1, 2, 3, 4, 5, 6]
j = 15
page_num = int(20000 / 15)
for i in range(page_num):
	comment_api = 'http://m.maoyan.com/mmdb/comments/movie/1217236.json?_v_=yes&offset={0}&startTime={1}%2021%3A09%3A31'.format(
		offset, startTime)
	s0 = Spidermaoyan(comment_api, startTime)
	json_comment = s0.get_json()
	if json_comment["total"] == 0:  # 当前时间内评论爬取完成
		if j < 9:  # 九月份(9天)
			startTime = '2018-09-%d' % day[j]
		elif j >= 9 and j < 15:  # 十月份(6天)
			startTime = '2018-10-%d' % day[j]
		else:  # 全部爬完
			break
		offset = 0
		j = j + 1
		continue
	s0.get_data(json_comment)
	offset = offset + 15
# time.sleep()

