# coding: UTF-8

from flask import Flask, render_template, request


import nltk
nltk.data.path.append('TA_REVIEW_ANALYZER/nltk_data')
sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."

tokens = nltk.word_tokenize(sentence)
print(tokens)
testing = tokens[4]
print(testing)

app = Flask(__name__)

@app.route('/')
def index():
    return testing
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
