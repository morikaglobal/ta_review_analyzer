from flask import Flask
from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
driver= webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)




app = Flask(__name__)

# @app.route('/', methods = ["GET", "POST"])
@app.route('/')

def index():
    driver.get("https://www.google.com")
    return (driver.page_source)
    # return ("Hello Hello")

 
if __name__ == '__main__':
      app.run()