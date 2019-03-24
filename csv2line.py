import csv
import os
import json
import requests
import coord_convert
import math

'''
1.读取原始轨迹
2.将GPS坐标转换为高德坐标系
3.进行轨迹纠偏
4.生成数据
'''
key = '高德 Web API Key'

def convertgps(lng, lat):
	res = coord_convert.wgs84_to_gcj02(float(lng), float(lat))
	return [res[0], res[1]]

#将13位时间戳转换为10位时间戳
def stamp13_2_10(time_stamp):
	return int(float(time_stamp)/1000)

#进行轨迹纠偏
def get_real_track(track):
	url = 'https://restapi.amap.com/v4/grasproad/driving?key='+key
	res = requests.post(url, json=track)
	return res.json()['data']['points']

csv_fp = list(csv.reader(open('lines.csv', encoding='utf-8')))
track = []
last_time_stamp = 0
name = csv_fp[0][0]

#读取原始轨迹并进行坐标转换
for i in range(len(csv_fp)-1):

	line = csv_fp[i]
	line2 = csv_fp[i+1]

	if i == 0:
		last_time_stamp = stamp13_2_10(line[8])-int(line[5])
		lnglat = convertgps(line[2], line[1])
		track.append({'x': lnglat[0], 'y': lnglat[1], 'sp': 60, 'ag': 0, 'tm': last_time_stamp})

	time_stamp = stamp13_2_10(line2[8])-int(line2[5])
	lnglat = convertgps(line2[2], line2[1])
	track.append({'x': lnglat[0], 'y': lnglat[1], 'sp': 60, 'ag': 0, 'tm': time_stamp-last_time_stamp})
	last_time_stamp = time_stamp

#轨迹纠偏
real_track = get_real_track(track)

#生成数据并删除异常值
line = []
for i in range(len(real_track)-1):
	p1 = real_track[i]
	p2 = real_track[i+1]
	length = math.sqrt(math.pow(p1['x']-p2['x'], 2)+math.pow(p1['y']-p2['y'], 2))
	if(length > 0.01):
		continue
	d = dict()
	d['name'] = name
	d['lnglat'] = [[p1['x'], p1['y']], [p2['x'], p2['y']]]

	line.append(d)

#写入文件
with open('linedatas.js', 'w', encoding='utf-8') as fp:
	fp.write('var lines = '+str(line))