import pickle
import numpy as np
import pandas as pd
from models.predict_model import predictResult
from settings import *
from sklearn import metrics
from visualization.visualize import *

if __name__ == '__main__':
	print("Reading testing data...")
	df_test = pd.read_csv(TEST_DATA,
		index_col=False, lineterminator='\n')
	X_test = df_test['text']
	Y_test = df_test['output_class']

	class_support = df_test.groupby('output_class').size()
	class_support = np.array(list(class_support))

	with open(FINAL_VECT, 'rb') as final_count_vect:
		count_vect = pickle.load(final_count_vect)
	with open(FINAL_TFIDF, 'rb') as final_tf_transformer:
		tf_transformer = pickle.load(final_tf_transformer)
	with open(FINAL_MODEL, 'rb') as final_model:
		lr_clf = pickle.load(final_model)

	obj = [count_vect, tf_transformer, lr_clf]
	print("Evaluating...")
	predicted = predictResult(X_test, obj)

	print("Accuracy: ", np.mean(predicted == Y_test))
	print("Classification report:\n", metrics.classification_report(Y_test, predicted))
	cm = metrics.confusion_matrix(Y_test, predicted)
	cm = (cm.T/class_support).T
	draw_confusion_matrix(cm, classes=['Hateful', 'Offensive', 'Clean'])
