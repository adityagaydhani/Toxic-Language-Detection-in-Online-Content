import config
import time
import numpy as np
import pandas as pd
from multiprocessing import Pool
from operator import itemgetter
from twython import Twython, TwythonError
from settings import *
from sklearn.model_selection import train_test_split

def authTwitter(consumer_key, consumer_secret,
	access_token, access_token_secret):
	global twitter
	twitter = Twython(consumer_key, consumer_secret,
	access_token, access_token_secret)

def getTweetFromID(id):
	try:
		dump_list = twitter.lookup_status(id = id)
	except TwythonError as e:
		print("TwythonError: {0}".format(e))
	else:
		tweet_dict = dict()
		for i in dump_list:
			tweet_dict[str(i["id"])] = i["text"]
		return tweet_dict

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def makeDataRaw(path=None):
	df_original_data = pd.read_csv(path, index_col = False)
	df_original_data = df_original_data[["tweet", "class"]]
	df_original_data.columns = column_names
	return df_original_data

def makeDataExternal1(path=None):
	df_external_data = pd.read_csv(path,
								index_col = False, encoding = "ISO-8859-1")
	df_external_data = df_external_data[["tweet_text",
										"does_this_tweet_contain_hate_speech"]]
	df_external_data.columns = column_names
	df_external_data.output_class = df_external_data.output_class.apply(
	lambda x: 0 if x == 'The tweet contains hate speech' else (
		1 if x == 'The tweet uses offensive language but not hate speech'
			else 2))
	return df_external_data

def makeDataExternal2(path=None):
	df_external_data_2 = pd.read_csv(path, header = None)

	# Modify column names and types
	df_external_data_2.columns = ["tweet_id", "output_class"]
	df_external_data_2.tweet_id = df_external_data_2.tweet_id.astype(str)

	# Drop the examples with clean class
	df_external_data_2 = df_external_data_2.drop(
		df_external_data_2[df_external_data_2.output_class == 'none'].index)
	df_external_data_2.output_class = df_external_data_2.output_class.apply(
		lambda x: 0)

	# Authenticate access to Twitter API
	consumer_key = config.consumer_key
	consumer_secret = config.consumer_secret
	access_token = config.access_token
	access_token_secret = config.access_token_secret
	authTwitter(consumer_key, consumer_secret,
		access_token, access_token_secret)

	# Prepare to get tweets from tweet IDs
	l = list(split(list(df_external_data_2.tweet_id),
		int(df_external_data_2.shape[0]/99)))
	with Pool(16) as pool:
		tweet_dump = pool.map(getTweetFromID, l)

	# Flat out tweet_dump into tweet_dict
	tweet_dict = dict()
	for d in tweet_dump:
		tweet_dict.update(d)

	keys = map(str, list(tweet_dict.keys()))

	#Drop the examples whos tweets are not retrived through API
	df_external_data_2 = df_external_data_2.drop(
		df_external_data_2[~df_external_data_2.tweet_id.isin(keys)].index)

	# Sort the dataset and retrived (id, tweet) items according to IDs
	df_external_data_2 = df_external_data_2.sort_values(['tweet_id'])
	tweet_tuples = list(tweet_dict.items())
	tweet_id, tweets = zip(*sorted(tweet_tuples, key = itemgetter(0)))
	tweet_id = list(tweet_id)
	tweets = list(tweets)

	# Assert if order of dataset keys match with order of retrived keys
	assert(tweet_id == list(df_external_data_2.tweet_id))

	# Add new column 'tweet' to the dataset
	df_external_data_2['tweet'] = tweets

	df_external_data_2 = df_external_data_2[["tweet", "output_class"]]
	df_external_data_2.columns = column_names

	return df_external_data_2

def combineData(frames=None):
	df_interim_data = pd.concat(frames)
	df_interim_data.text = list(df_interim_data.text.astype(str))
	df_interim_data.output_class = list(
		df_interim_data.output_class.astype(int))
	df_interim_data.to_csv(INTERIM_DATA, sep=',', index=False, encoding="utf-8")
	print("Dataset stored in ", INTERIM_DATA)
	return df_interim_data

def generateTrainAndTestFiles(df=None):
	sample_size = max(df.groupby('output_class').size())
	df_0 = df.loc[df.output_class == 0].sample(
		sample_size, replace=True)
	df_1 = df.loc[df.output_class == 1].sample(
		sample_size, replace=True)
	df_2 = df.loc[df.output_class == 2].sample(
		sample_size, replace=True)
	df = pd.concat([df_0, df_1, df_2])

	X_train, X_test, Y_train, Y_test = train_test_split(
		df.text.values, df.output_class.values, test_size=0.3, random_state=21)

	df_train = pd.DataFrame({'text': X_train, 'output_class' : Y_train})
	df_test = pd.DataFrame({'text': X_test, 'output_class' : Y_test})

	df_train.to_csv(TRAIN_DATA, sep=',', index=False)
	df_test.to_csv(TEST_DATA, sep=',', index=False)

	print("Training data stored in ", TRAIN_DATA)
	print("Testing data stored in ", TEST_DATA)

column_names = ["text", "output_class"]
twitter = None

if __name__ == "__main__":
	print("Reading raw data...")
	df_original_data = makeDataRaw(RAW_DATA)

	print("Reading data from external sources...")
	df_external_data = makeDataExternal1(EXTERNAL_DATA_1)
	df_external_data_2 = makeDataExternal2(EXTERNAL_DATA_2)

	print("Making dataset...")
	df_interim_data = combineData(
		frames = [df_original_data, df_external_data, df_external_data_2])

	print("Generating training and testing data files...")
	generateTrainAndTestFiles(df = df_interim_data)