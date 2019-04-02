import build_features

testcases = ['Hello world', 'How are you?','My name is John']


def test_generateNGramValues():
	X_train_counts = build_features.generateNGramValues(testcases)
	if not X_train_counts:
		a=1
	else:
		a=0

	assert a == 0

X_train_counts = build_features.generateNGramValues(testcases)

def test_generateTFIDFValues():
	X_train_tfidf = build_features.generateTFIDFValues(X_train_counts)
	if not X_train_tfidf:
		a = 1
	else:
		a = 0

	assert a == 0

