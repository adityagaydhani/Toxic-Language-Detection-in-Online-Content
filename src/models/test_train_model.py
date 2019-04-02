import train_model
import pickle
import predict_model
import numpy as np 
import pandas as pd
from settings import *

def test_getdata(df_train=pd.read_csv(TRAIN_DATA, index_col=False, lineterminator="\n")):
	X_train,Y_train = train_model.getdata(df_train)
	x_train = df_train['text']
	y_train = df_train['output_class']
	assert X_train.all() == x_train.all()
	assert Y_train.all() == y_train.all()
