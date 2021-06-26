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

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')

driver= webdriver.Chrome(executable_path=r'C:/Users/USER/chromedriver.exe', chrome_options=chrome_options)


app = Flask(__name__)

@app.route('/')
def index():    
    
    url = "http://www.yahoo.co.jp"
    driver.get(url)
    return ("Hello Hello World")
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
