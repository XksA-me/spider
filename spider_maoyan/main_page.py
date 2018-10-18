'''
data : 2018.10.06
author : 极简XksA
goal : 爬取猫眼《悲伤逆流成河》影评，词云可视化
'''

# 猫眼电影介绍url
# http://maoyan.com/films/1217236

import requests,time,random
# from fake_useragent import UserAgent
import json,csv,os
import pandas as pd

USER_AGENTS = [ "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)", "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)", "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)", "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)", "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)", "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1", "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0", "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20", "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52", ]

class Spidermaoyan():
	headers = {
		    "User-Agent": random.choice(USER_AGENTS),
		    "Host":"m.maoyan.com",
		    "Referer":"http://m.maoyan.com/movie/1217236/comments?_v_=yes"
		}
	
	def __init__(self,url,time):
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
	def get_data(self,json_comment):
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
			list_one = [self.time,nickName,gender,cityName,userLevel,score,content]
			list_info.append(list_one)
		print(list_info)
		self.file_do(list_info)
	
	# 存储文件
	def file_do(self,list_info):
		# 获取文件大小
		file_size = os.path.getsize(r'G:\maoyan\maoyan.csv')
		if file_size == 0:
			# 表头
			name = ['评论日期', '评论者昵称', '性别', '所在城市','猫眼等级','评分','评论内容']
			# 建立DataFrame对象
			file_test = pd.DataFrame(columns=name, data=list_info)
			# 数据写入
			file_test.to_csv(r'G:\maoyan\maoyan.csv', encoding='utf_8_sig', index=False)
		else:
			with open(r'G:\maoyan\maoyan.csv', 'a+',encoding='utf_8_sig', newline='') as file_test:
				# 追加到文件后面
				writer = csv.writer(file_test)
				# 写入文件
				writer.writerows(list_info)

def spider_maoyan():
	# 猫眼电影短评接口
	offset = 0
	# 电影是2018.9.21上映的
	startTime = '2018-09-21'
	day = [22,23,24,25,26,27,28,29,30,1,2,3,4,5,6]
	j = 0
	page_num = int(20000/15)
	for i in range(page_num):
		comment_api = 'http://m.maoyan.com/mmdb/comments/movie/1217236.json?_v_=yes&offset={0}&startTime={1}%2021%3A09%3A31'.format(offset,startTime)
		s0 = Spidermaoyan(comment_api,startTime)
		json_comment = s0.get_json()
		if json_comment["total"] == 0: # 当前时间内评论爬取完成
			if j < 9:  # 九月份(9天)
				startTime = '2018-09-%d'%day[j]
			elif j >= 9 and j < 15:  # 十月份(6天)
				startTime = '2018-10-%d'%day[j]
			else: # 全部爬完
				break
			offset = 0
			j = j + 1
			continue
		s0.get_data(json_comment)
		offset = offset + 15
		# time.sleep(1)
	

if __name__ == '__main__':
	spider_maoyan()
	