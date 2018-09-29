import KITTI_data_load_from_file
from pymongo import MongoClient
import pandas as pd


def get_data_from_mongo(folder_name):
	# open connection
	connection = MongoClient()

	# get db
	db = connection.study

	# get DB data from mongoDB to dataframe
	query = {'file_id': folder_name}
	df_data = pd.DataFrame.from_records(db.ML201809.find(query))

	# delete DB id
	del df_data['_id']

	print df_data

	return df_data


def put_data_to_mongo(df_data):

	try:
		# open connection
		connection = MongoClient()

		# get db
		db = connection.study

		# insert df into <table> of <dataframe>
		db.ML201809.insert_many(df_data.to_dict('records'))

	except Exception as e:
		print e


if __name__ == '__main__':
	folder_name = "oxts_02"

	try:
		df_data = get_data_from_mongo(folder_name)
	except Exception as e:
		print e
		df_data = pd.DataFrame()

	if len(df_data.index) == 0:
		print "no data in mongoDB. load from files.."
		# empty data
		df_data = KITTI_data_load_from_file.get_data_from_file(folder_name)
		put_data_to_mongo(df_data)

	# df_data.to_csv("test_csv.csv")

	KITTI_data_load_from_file.plot_dataframe(df_data)
