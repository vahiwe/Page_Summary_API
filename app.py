from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from flask import Flask, request, jsonify,render_template

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 10

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/api/summarize', methods=['POST'])
def summarize():
    """ Returns summary of articles """
    if request.method == 'POST':
        url = request.form['pageurl']
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        final = []

        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            final.append(str(sentence))
        return render_template('result.html', len=len(final), summary=final)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)