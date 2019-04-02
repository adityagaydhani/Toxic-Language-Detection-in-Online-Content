import config
import time
import numpy as np
import pandas as pd
from multiprocessing import Pool
from operator import itemgetter
from twython import Twython, TwythonError
from settings import *
from sklearn.model_selection import train_test_split
import make_dataset
import preprocess_data as pr


df_org = pd.read_csv(RAW_DATA,index_col=False)
df_org = df_org[["tweet","class"]]

def test_makeDataRaw():
	df_original = make_dataset.makeDataRaw(RAW_DATA)
	assert df_org["tweet"].all() == df_original["text"].all()
	assert df_org["class"].all() == df_original["output_class"].all()

df_external_data = pd.read_csv(EXTERNAL_DATA_1,index_col = False, encoding = "ISO-8859-1")
df_external_data = df_external_data[["tweet_text",
										"does_this_tweet_contain_hate_speech"]]
df_external_data.columns = ["text","output_class"]
df_external_data.output_class = df_external_data.output_class.apply(
lambda x: 0 if x == 'The tweet contains hate speech' else (
	1 if x == 'The tweet uses offensive language but not hate speech'
		else 2))

def test_makeDataExternal1():
	df_external_data_final = make_dataset.makeDataExternal1(EXTERNAL_DATA_1)
	assert df_external_data_final["text"].all() == df_external_data["text"].all()
	assert df_external_data_final["output_class"].all() == df_external_data["output_class"].all()

df_external_data_2 = make_dataset.makeDataExternal2(EXTERNAL_DATA_2)
#df_interim_data = make_dataset.combineData(frames = [df_org,df_external_data,df_external_data_2])


def test_generateTrainAndTestFiles():
	make_dataset.generateTrainAndTestFiles(df_interim_data = make_dataset.combineData(frames = [df_org,df_external_data,df_external_data_2]))
	if TRAIN_DATA and TEST_DATA:
		a=1
	else:
		a=0
	assert a == 1

"""def test_preprocess():
	result = pr.preprocess("Hello world")
	assert result == "Hello world" """

