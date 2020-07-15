from flask import Flask

import os
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

URL = 'https://google.com/'




app = Flask(__name__)

@app.route('/')
def index():

    try:
        driver.get(URL)
        return("hohoho success" + URL)
    except:
        return ("Error Error")
    finally:
        driver.close()



if __name__ == '__main__':
      app.run()