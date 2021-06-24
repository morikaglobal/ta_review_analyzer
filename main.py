# coding: UTF-8

# from flask import Flask, render_template, request
# import nltk
# nltk.data.path.append('TA_REVIEW_ANALYZER/nltk_data')
# sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."

# tokens = nltk.word_tokenize(sentence)
# print(tokens)
# testing = tokens[4]
# print(testing)

import logging
import os

from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return ("Hello World")
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
