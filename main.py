from flask import Flask

import os
from selenium import webdriver

# chrome driverの配置場所を設定
CHROME_DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

# ダウンロードフォルダ―の場所を設定・作成
DOWNLOAD_DIR = '/app/tmp'
os.mkdir(DOWNLOAD_DIR)
print(DOWNLOAD_DIR)

# chromeの起動オプションを設定
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('start-maximized')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# chromeの追加設定(driverの場所やファイル等のダウンロード先)
prefs = {'download.default_directory': DOWNLOAD_DIR,
         'download.prompt_for_download': False}
options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH,
                           options=options)
browser.command_executor._commands['send_command'] = ('POST',
                                                      '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior',
          'params': {'behavior': 'allow',
                     'downloadPath': DOWNLOAD_DIR}}
browser.execute('send_command', params)



app = Flask(__name__)

@app.route('/')
def index():

    try:
        URL = 'https://google.com/'
        browser.get(URL)
        return("hohoho success" + URL)
    except:
        return ("Error Error")
    finally:
        browser.close()



if __name__ == '__main__':
      app.run()