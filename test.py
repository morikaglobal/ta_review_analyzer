from flask import Flask, render_template, request
import requests
from forms import UrlSearchForm

import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# commented out for heroku deployment
driver_location = r"C:\Users\masao\Anaconda3\chromedriver.exe"

options = webdriver.ChromeOptions()

options.add_argument('--lang=en')
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=driver_location, options=options)










app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():

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
                errors.append(
                "Loading."
                ) 
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
        print("working")
        driver.get(search_string)
        print("getting")
        
        
        
        # driver.implicitly_wait(10)
        
        # return("Success")
        container = driver.find_elements_by_xpath('//q[@class="IRsGHoPm"]')
        print(container)
        num_page_items = len(container)
        title = driver.find_elements_by_xpath('//div[@class="glasR4aX"]')

        for j in range(num_page_items):
            reviewtitle = title[j]
            print(reviewtitle.text)
        
        # return (reviewtitle.text)
        # driver.get(search_string)
        # time.sleep(30)

        # container = driver.find_elements_by_xpath('//q[@class="location-review-review-list-parts-ExpandableReview__reviewText--gOmRC"]')
        # container = driver.find_elements_by_xpath('//q[@class="IRsGHoPm"]')
        # print(container)


        return render_template("results.html", search_string = search_string)
        # return("hohoho success" + URL)
    except:
        return ("Error Error")
    finally:
        driver.quit()

    # driver.get(search_string)
    # time.sleep(30)
    # # return("success: " + search_string)
    # # driver.quit()

    # return render_template("results.html", search_string = search_string)

    

if __name__ == '__main__':
      app.run()