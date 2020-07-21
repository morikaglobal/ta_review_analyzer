from flask import Flask, render_template, request
import requests
from forms import UrlSearchForm

from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
driver= webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)




app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    # driver.get("https://www.google.com")
    # return (driver.page_source)
    # return ("Hello Hello")

    errors = []
    urlsearch = UrlSearchForm(request.form)
    search_string = urlsearch.data['search']

    if request.method == "POST":
    
        
        try:

            #test
            # driver.get(search_string)
            # errors.append(
            #     "Getting URL"
            # )   
            
            
            # driver.implicitly_wait(10)
            if search_string.startswith("https://www.tripadvisor.com/", 0):
                # errors.append(
                # "Loading."
                # ) 
                return search_results(urlsearch)

            else:
                errors.append(
                "Unable to get the URL.  Please paste a valid Tripadvisor URL link."
                ) 

            
            
            

            
            
            # return search_results(urlsearch)
        except:
            errors.append(
                "Unable to get the URL.  Please paste a valid Tripadvisor URL link."
            )       
    return render_template("index.html", form = urlsearch, errors = errors)

def search_results(urlsearch):
    
    urlsearch = UrlSearchForm(request.form)
    search_string = urlsearch.data['search']


    try:
        # return ("success: " + search_string)
        # print("working")
        driver.get(search_string)
        # print("getting")
        
        
        
        # # driver.implicitly_wait(10)
        
        # # return("Success")
        container = driver.find_elements_by_xpath('//q[@class="IRsGHoPm"]')
        # print(container)
        num_page_items = len(container)
        title = driver.find_elements_by_xpath('//div[@class="glasR4aX"]')

        for j in range(num_page_items):
            reviewtitle = title[j]
            # print(reviewtitle.text)
        
        title = reviewtitle.text
        # return (reviewtitle.text)
        # driver.get(search_string)
        # time.sleep(30)

        # container = driver.find_elements_by_xpath('//q[@class="location-review-review-list-parts-ExpandableReview__reviewText--gOmRC"]')
        # container = driver.find_elements_by_xpath('//q[@class="IRsGHoPm"]')
        # print(container)


        return render_template("results.html", search_string = search_string, title = title)
        # return("hohoho success" + URL)
    except:
        return ("Error Error")
    finally:
        driver.quit()

 
if __name__ == '__main__':
      app.run()