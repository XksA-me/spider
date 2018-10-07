'''
参考：http://blog.51cto.com/12402007/2161698?wx=
对地理位置进行地图可视化，主要解决了部分地级市不能显示的问题
'''
# 处理地名数据，解决坐标文件中找不到地名的问题
import json

# 导入Style类，用于定义样式风格
from pyecharts import Style
# 导入Geo组件，用于生成地理坐标类图
from pyecharts import Geo
import json
# 导入Geo组件，用于生成柱状图
from pyecharts import Bar
# 导入Counter类，用于统计值出现的次数
from collections import Counter
import csv
from os import path

cityName = []

d=path.dirname(__file__)
def read_csv():
	content = ''
	# 读取文件内容
	with open(r'G:\maoyan\maoyan.csv', 'r', encoding='utf_8_sig', newline='') as file_test:
		# 读文件
		reader = csv.reader(file_test)
		i = 0
		for row in reader:
			if i != 0:
				cityName.append(row[3])
				# print(row)
			i = i + 1
		print('一共有：' + str(i - 1) + '个')

# 数据可视化
def render_city(cities):
    # 对城市数据和坐标文件中的地名进行处理
    handle(cities)
    data = Counter(cities).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表
    print(data)

    # 定义样式
    style = Style(
        title_color='#fff',
        title_pos='center',
        width=1200,
        height=600,
        background_color='#404a59'
    )

    # 根据城市数据生成地理坐标图
    geo = Geo('《悲伤逆流成河》粉丝位置分布',  **style.init_style)
    attr, value = geo.cast(data)
    geo.add('', attr, value, visual_range=[0, 600],
            visual_text_color='#fff', symbol_size=15,
            is_visualmap=True, is_piecewise=True, visual_split_number=10)
    geo.render(d+'/picture/geo.html')

def handle(cities):
    # 获取坐标文件中所有地名
    data = None
    with open(d+'/static/city_coordinates.json',mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json

    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)
        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                # print(k, city)
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break
        # 处理不存在的地名
        if count == len(data):
            while city in cities:
                cities.remove(city)

    # print(len(data), len(data_new))

    # 写入覆盖坐标文件
    with open(r'H:\学习资源\Python\框架学习\Virtualenv\flask\flask-env\Lib\site-packages\pyecharts\datasets\city_coordinates.json',mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))  # 将json转换为str
read_csv()
render_city(cityName)