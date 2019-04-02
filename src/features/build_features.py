from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from data.preprocess_data import *

def generateNGramValues(X_train):
	count_vect = CountVectorizer(ngram_range=(1, 3), stop_words='english',
		preprocessor=preprocess, lowercase=True)
	X_train_counts = count_vect.fit_transform(X_train)
	return [X_train_counts, count_vect]

def generateTFIDFValues(X_train_counts):
	tf_transformer = TfidfTransformer(norm='l2', use_idf=True,
		smooth_idf=True, sublinear_tf=False)
	X_train_tfidf = tf_transformer.fit_transform(X_train_counts)
	return [X_train_tfidf, tf_transformer]