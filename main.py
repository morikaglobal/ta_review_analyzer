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

# @app.route('/')

# def index():
#     return ("Hello")

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
        scraped_data = []
        location = []

        for i in range (0, 1):
            # driver.get(search_string)
            # driver.implicitly_wait(10)
            
            # return("Success")
            container = driver.find_elements_by_xpath('//q[@class="IRsGHoPm"]')
            # print("container : ")
            # print(container)
            num_page_items = len(container)
            title = driver.find_elements_by_xpath('//div[@class="glasR4aX"]')
            # return(num_page_items)
            reviewer_location = driver.find_elements_by_xpath('//span[@class="default _3J15flPT small"]')
            location_div = driver.find_elements_by_xpath('//div[@class="_1EpRX7o3"]')
            return(search_string)

            for j in range(num_page_items):
                print("processing: ")

                list = {}

        
                # list['title'] = title[j].text
                # print(list['title'])
                # print(title[j].text)
                list['reviewtitle'] = title[j].text
                print(title[j].text)

                list['reviewtext'] = container[j].text

                try:
                    locationtext = location_div[j].find_element_by_xpath('.//span[@class="default _3J15flPT small"]')
                    print(locationtext.text)
                    location.append(locationtext.text)
                except:
                    print("no location")
                    location.append("no location")


                scraped_data.append(list)

                # print("scraped_data for this page is: ")
                # # print(type(scraped_data)) #list
                # print(scraped_data)

            print("scraped_data: ")
            print(type(scraped_data)) #list
            print(scraped_data)

            driver.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
            print("clicked")
            time.sleep(50)

        print("collected data: ")
        print(type(scraped_data)) #list
        print(scraped_data)
        print("location list: ")
        print(type(location))
        print(location)
        print("First set: ")
        print(scraped_data[0])
        print(location[0])
            
        # return ('hohoho')

        

        
        # for data in scraped_data:
        #     print(data.reviewtitle)

        # test = scraped_data[0]['reviewtitle']
        # return test
        # return render_template('test.html',
        #                         search_string = search_string,
        #                         scraped_data = scraped_data)



        # todos = ['牛乳を買う', '洗濯をする', '掃除をする']
        return ("ohoho")
        return render_template("test2.html", search_string = search_string, location = location)
        return render_template("test.html", search_string = search_string)
        
        
        # return render_template("results.html", search_string = search_string)
        # return(list['title'])
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
