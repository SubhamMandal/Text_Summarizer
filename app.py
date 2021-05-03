from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from flask import Flask, render_template, request


app = Flask(__name__)
app.static_folder = 'static'

def getSummary(text):
	try:
		try:
			punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
			stopwords= list(STOP_WORDS)
		except:
			return "problem in punctuation"
		try:
			import en_core_web_sm
		except:
			return "couldn't import"
		try:
			nlp = en_core_web_sm.load()
		except:
			return "problem in npl"
		doc=nlp(text)
		try:
			tokens=[token.text for token in doc]
			word_frequencies={}
			for word in doc:
				if word.text.lower() not in stopwords:
					if word.text.lower() not in punctuation:
						if word.text not in word_frequencies.keys():
							word_frequencies[word.text]=1
						else:
							word_frequencies[word.text]+=1
		except:
			return "problem in algo"
	except:
		return "problem in first half"

	try:
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

		try:
			from heapq import nlargest
		except:
			return "heapq not found"
		select_length = int(len(sentence_tokens)*0.2)
		summary= nlargest(select_length,sentence_scores,key=sentence_scores.get)
		final_sum=[word.text for word in summary]
		summary=' '.join(final_sum)
	except:
		return "problem in second half"

	return summary

@app.route('/')
def hello():
	return render_template("home_page.html")


@app.route('/', methods = ['POST'])
def display():
	text = request.form['passage']
	try:
		summary = getSummary(text)
	except:
		summary = "there has been some error"
	return render_template("summary_page.html", summary= summary)

@app.route('/file', methods = ['POST'])
def filedisplay():
	f = request.files['userfile']
	path = "./static/{}".format(f.filename)
	f.save(path)
	myfile = open(path, "r", encoding="utf8")
	text = myfile.read()
	try:
		summary = getSummary(text)
	except:
		summary = "error"
	return render_template("summary_page.html", summary= summary)


if __name__ == '__main__':
	app.debug = True
	app.run()
