from flask import Flask, render_template, request

from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

# options = webdriver.ChromeOptions()
chrome_options.add_argument('--lang=en')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu');
chrome_options.add_argument('--disable-extensions');
chrome_options.add_argument('--proxy-server="direct://"');
chrome_options.add_argument('--proxy-bypass-list=*');
chrome_options.add_argument('--start-maximized');


# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)

app = Flask(__name__)

# @app.route('/', methods = ["GET", "POST"])
@app.route('/')

def index():
    return ("Hello Hello")

 
if __name__ == '__main__':
      app.run()


# from flask import Flask, render_template, request
# import requests
# from forms import UrlSearchForm

# import time
# import os
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException


# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
# chrome_options.add_argument('--headless')
# # chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument('--no-sandbox')
# #error on heroku happens from codes below
# driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
# # driver.get("https://google.com/")

# # URL = 'https://google.com/'

# app = Flask(__name__)

# # @app.route('/', methods = ["GET", "POST"])
# @app.route('/')

# def index():
#     return ("Hello Hello")

 
# if __name__ == '__main__':
#       app.run()

