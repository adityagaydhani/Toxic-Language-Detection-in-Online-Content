import re
from nltk.stem.porter import *

stemmer = PorterStemmer()
def preprocess(text_string):
	space_pattern = '\s+'
	giant_url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
		'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	mention_regex = '@[\w\-]+'
	retweet_regex = '^[! ]*RT'
	parsed_text = re.sub(space_pattern, ' ', text_string)
	parsed_text = re.sub(giant_url_regex, '', parsed_text)
	parsed_text = re.sub(mention_regex, '', parsed_text)
	parsed_text = re.sub(retweet_regex, '', parsed_text)
	stemmed_words = [stemmer.stem(word) for word in parsed_text.split()]
	parsed_text = ' '.join(stemmed_words)
	return parsed_text