# coding: UTF-8

# import logging
# import os

from flask import Flask
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

# logging.basicConfig(level=logging.INFO)
# logger=logging.getLogger(__name__)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--no-sandbox')

# driver= webdriver.Chrome(executable_path=r'C:/Users/USER/chromedriver.exe', chrome_options=chrome_options)



app = Flask(__name__)

@app.route('/')
def index(): 

    # url = "http://www.yahoo.co.jp"
    # driver.get(url)   
    
    return ("Hello Hello World mainpy working")
    


if __name__ == "__main__":
    app.run()
