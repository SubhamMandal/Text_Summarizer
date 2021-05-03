from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from flask import Flask, render_template, request


app = Flask(__name__)
app.static_folder = 'static'

def getSummary(text):
	stopwords= list(STOP_WORDS)
	import en_core_web_sm
	nlp = en_core_web_sm.load()
	doc=nlp(text)
	tokens=[token.text for token in doc]
	word_frequencies={}
	for word in doc:
		if word.text.lower() not in stopwords:
			if word.text.lower() not in punctuation:
				if word.text not in word_frequencies.keys():
					word_frequencies[word.text]=1
				else:
					word_frequencies[word.text]+=1

	max_frequency=max(word_frequencies.values())
	for word in word_frequencies.keys():
		word_frequencies[word]=word_frequencies[word]/max_frequency

	sentence_tokens=[sent for sent in doc.sents]
	sentence_scores={}
	for sent in sentence_tokens:
		for word in sent:
			if word.text.lower() in word_frequencies.keys():
				if sent not in sentence_scores.keys():
					sentence_scores[sent]=word_frequencies[word.text.lower()]
				else:
					sentence_scores[sent]+=word_frequencies[word.text.lower()]

	from heapq import nlargest
	select_length = int(len(sentence_tokens)*0.2)
	summary= nlargest(select_length,sentence_scores,key=sentence_scores.get)
	final_sum=[word.text for word in summary]
	summary=' '.join(final_sum)

	return summary

@app.route('/')
def hello():
	return render_template("home_page.html")


@app.route('/', methods = ['POST'])
def display():
	text = request.form['passage']
	summary = getSummary(text)
	summary = "working"
	return render_template("summary_page.html", summary= summary)


if __name__ == '__main__':
	app.debug = True
	app.run()
