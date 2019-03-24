import csv
import coord_convert

'''
将百度坐标系转换成高德坐标系
'''
csv_fp = list(csv.reader(open('stations.csv', encoding='utf-8')))
stations = []
for station in csv_fp:
	d = dict()
	d['name'] = station[0]
	lnglat = coord_convert.bd09_to_gcj02(float(station[1]), float(station[2]))
	d['lnglat'] = [lnglat[0], lnglat[1]]
	stations.append(d)

#写入文件
with open('stations.js', 'w', encoding='utf-8') as fp:
	fp.write('var stations = '+str(stations))