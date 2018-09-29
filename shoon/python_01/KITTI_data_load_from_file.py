import glob
import time
from dateutil.parser import parse
import pandas as pd
import matplotlib.pyplot as plt
import pyproj
import KITTI_data_load_from_mongo


def get_data_from_file(folder_name):
	# load file name
	file_list = glob.glob("{}/data/*.txt".format(folder_name))
	file_list_sorted = []
	for inx in range(0, len(file_list)):
		string = "{}/data/{:010d}.txt".format(folder_name, inx)
		file_list_sorted.append(string)

	# print file_list_sorted

	# timestamp conversion
	f_timestamp = open("{}/timestamps.txt".format(folder_name), 'r')
	timestamp_str_list = []
	timestamp_list = []
	while True:
		line = f_timestamp.readline()
		if not line: break
		line = line.replace("\n", "")
		sec_remain = line.split(".")[-1]
		sec_remain = float(sec_remain) * 1e-9
		date_time = parse(line)
		timestamp = time.mktime(date_time.timetuple())

		timestamp_str_list.append(line)
		timestamp_list.append(timestamp + sec_remain)

	f_timestamp.close()

	# print timestamp_list

	# make dataframe
	keys_list = """lat lon alt
	roll pitch yaw
	vn ve vf vl vu ax ay az af al au
	wx wy wz wf wl wu
	pos_accuracy vel_accuracy navstat numsats posmode velmode orimode
	timestamp timestamp_string
	file_id""".split()

	df_data = pd.DataFrame(columns=keys_list)

	for inx in range(0, len(file_list_sorted)):
		f_ = open(file_list_sorted[inx], 'r')

		line = f_.readline()
		line = line.replace('\n', '')
		data_line = line.split(' ')

		data_float = [float(str) for str in data_line]
		data_float.append(timestamp_list[inx])
		data_float.append(timestamp_str_list[inx])
		data_float.append(folder_name)

		df_data.loc[inx] = data_float

		f_.close()

	print df_data

	return df_data


def plot_dataframe(df_data):
	# a scatter plot comparing num_children and num_pets
	df_data.plot(kind='scatter', x='lat', y='lon', color='red')
	plt.savefig('latlon.png')

	wgs84 = pyproj.Proj("+init=EPSG:4326")  # LatLon with WGS84 datum used by GPS units and Google Earth
	rgf93 = pyproj.Proj("+init=EPSG:2154")
	xx, yy = pyproj.transform(wgs84, rgf93, df_data['lon'].tolist(), df_data['lat'].tolist())

	plt.figure()
	plt.scatter(xx, yy, color='red')
	plt.axis('equal')
	plt.savefig('2D.png')


if __name__ == '__main__':
	folder_name = "oxts_09"

	df_data = get_data_from_file(folder_name)

	# df_data.to_csv("test_csv.csv")

	plot_dataframe(df_data)


