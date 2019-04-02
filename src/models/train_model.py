import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from features.build_features import *
from settings import *

def getdata(df_train):
	x_train,y_train=df_train['text'],df_train['output_class']
	return x_train,y_train

if __name__ == '__main__':
	print("Reading training data...")
	df_train = pd.read_csv(TRAIN_DATA, index_col=False,
		lineterminator='\n')
	X_train, Y_train = getdata(df_train)
	# X_train = df_train['text']
	# Y_train = df_train['output_class']

	print("Building features...")
	print("Generating n-gram values...")
	print("Generating TFIDF values...")
	X_train_counts, count_vect = generateNGramValues(X_train)
	X_train_tfidf, tf_transformer = generateTFIDFValues(X_train_counts)

	print("Training model...")
	log_regression = LogisticRegression(C=100, class_weight='balanced',
		solver='liblinear', penalty='l2', max_iter=100, multi_class='ovr')
	lr_clf = log_regression.fit(X_train_tfidf, Y_train)
	print("Model trained.")
	
	# Save features and models for predicting
	with open(FINAL_VECT, 'wb') as final_count_vect:
		pickle.dump(count_vect, final_count_vect, pickle.HIGHEST_PROTOCOL)
	with open(FINAL_TFIDF, 'wb') as final_tf_transformer:
		pickle.dump(tf_transformer, final_tf_transformer, pickle.HIGHEST_PROTOCOL)
	with open(FINAL_MODEL, 'wb') as final_model:
		pickle.dump(lr_clf, final_model, pickle.HIGHEST_PROTOCOL)
