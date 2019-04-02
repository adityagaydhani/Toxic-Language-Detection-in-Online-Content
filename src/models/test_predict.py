import train_model
import pickle
import predict_model
import numpy as np 
import pandas as pd
from settings import *


with open(FINAL_VECT,'rb') as final_count_vect:
	count_vect = pickle.load(final_count_vect)
with open(FINAL_TFIDF, 'rb') as final_tf_transformer:
	tf_transformer = pickle.load(final_tf_transformer)
with open(FINAL_MODEL, 'rb') as final_model:
	lr_clf = pickle.load(final_model)
obj = [count_vect, tf_transformer, lr_clf]

input_list = ["Hello there"," " ,"asshole","black nigger","hero"]
output_list = [2,1,1,0,2]
def test_predictResult():
	for i in range(0,len(input_list)):
		if input_list[i]==" ":
			predicted_class = predict_model.predictResult([input_list[i]],obj)
			assert predicted_class == 1
		else:
			predicted_class = predict_model.predictResult([input_list[i]],obj)
			assert predicted_class == output_list[i]
