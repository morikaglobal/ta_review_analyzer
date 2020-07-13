from flask import Flask, render_template, request
import requests
from forms import UrlSearchForm

import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# import nltk
# nltk.download("punkt")

# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
# ps = PorterStemmer()

# from textblob import TextBlob
# from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
# from pprint import pprint
# import pandas as pd
# import numpy as np
# import seaborn as sns
# sns.set(style='darkgrid', context='talk', palette='Dark2')

# commented out for heroku deployment
# driver_location = r"C:\Users\masao\Anaconda3\chromedriver.exe"
driver_path = '/app/.chromedriver/bin/chromedriver'

# os.environ['PATH'] += ':'+os.path.dirname(os.path.realpath(__file__))+"/webdrivers"

options = webdriver.ChromeOptions()
options.add_argument('--lang=en')
options.add_argument('--headless')
options.add_argument('--disable-gpu');
options.add_argument('--disable-extensions');
options.add_argument('--proxy-server="direct://"');
options.add_argument('--proxy-bypass-list=*');
options.add_argument('--start-maximized');
driver = webdriver.Chrome(executable_path=driver_path, options=options)
# driver = webdriver.Chrome(options=options)




app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    errors = []
    urlsearch = UrlSearchForm(request.form)

    if request.method == "POST":
        
        try:
            return search_results(urlsearch)
        except:
            errors.append(
                "Unable to get the URL.  Please paste a valid Tripadvisor URL link."
            )       
    return render_template("index.html", form = urlsearch, errors = errors)

def search_results(urlsearch):

    urlsearch = UrlSearchForm(request.form)
    search_string = urlsearch.data['search']
    
    driver.get(search_string)
    return("success: " + search_string)
    driver.quit()

    # return render_template("results.html", search_string = search_string)


    # article = Article(search_string)

    # article.download()
    # article.parse()
    # # nltk.download("punkt")
    # article.nlp()

    # data = article.text
    # title = article.title
    # date = article.publish_date
    # published_date = date.strftime("%d %B %Y")
    # author = article.authors[0]

    # image = article.top_image

    # # WordCloud disabled for now
    # # cloud = get_wordcloud(data)
    # keyword = article.keywords

    # summary = article.summary

    # return render_template("results.html", search_string = search_string, title = title, published_date=published_date, author = author, image = image, keyword = keyword, summary = summary)

if __name__ == '__main__':
      app.run()