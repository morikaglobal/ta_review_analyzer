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

from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from pprint import pprint
import pandas as pd
import numpy as np
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')

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

        # return (search_string)

        for i in range (0, 1):
            # driver.get(search_string)
            # driver.implicitly_wait(10)
            read_more = driver.find_element_by_class_name("_36B4Vw6t")
            read_more.click()
            
            # return("Success")
            container = driver.find_elements_by_xpath('//q[@class="IRsGHoPm"]')
            # print("container : ")
            # print(container)
            
            num_page_items = len(container)
            title = driver.find_elements_by_xpath('//div[@class="glasR4aX"]')
            # return(num_page_items)
            reviewer_location = driver.find_elements_by_xpath('//span[@class="default _3J15flPT small"]')
            location_div = driver.find_elements_by_xpath('//div[@class="_1EpRX7o3"]')
            # return(search_string)

            for j in range(num_page_items):
                print("processing: ")

                list = {}

        
                # list['title'] = title[j].text
                # print(list['title'])
                # print(title[j].text)
                list['reviewtitle'] = title[j].text
                print(title[j].text)
                # return (title[j].text) worked on the web



                list['reviewtext'] = container[j].text
                lowercase_text = container[j].text.lower()

                # # removing puncutations
                # testwords = nltk.word_tokenize(lowercase_text)
                # test_words = [word for word in testwords if word.isalnum()]
                # list['reviewtext'] = test_words
                # # print("puncutations removed: ")
                # # print(test_words)

                # spelling_corrected = []

                # #spelling correction
                # for word in test_words:
                #     if word == "disney" or "hong" or "kong" or "hk": 
                #         spelling_corrected.append(word)
                #     else:
                #         output = str(TextBlob(word).correct())
                #         spelling_corrected.append(word)

                # print("spelling_corrected: ")
                # print(type(spelling_corrected))

                # #breaking down words by words
                # stop_words = set(stopwords.words("english"))
                # # word_tokens = word_tokenize(lowercase_text)
                # corrected_text = ' '.join(spelling_corrected)
                # word_tokens = word_tokenize(corrected_text)
                # # print(word_tokens)

                # # filtering and removing stop words
                # filtered_text = [w for w in word_tokens if not w in stop_words]

                # filtered_text = []

                # # removing stop words and stemming
                # stemmed = []
                
                # for w in word_tokens:
                #     if w not in stop_words:
                        
                #         filtered_text.append(w)
                #         stemmed_text = ps.stem(w)
                #         stemmed.append(stemmed_text)

                        
                # print("stop words removed: ")
                # # print(filtered_text)
                # data_for_commonwords.append(filtered_text)

        
                # stemmed_text = ' '.join(stemmed)
                # print("stemmed: ")
                # # print(stemmed_text)
                
                # reviewtext_to_analyze.append(stemmed_text)

                try:
                    locationtext = location_div[j].find_element_by_xpath('.//span[@class="default _3J15flPT small"]')
                    print(locationtext.text)
                    location.append(locationtext.text)
                    # return locationtext.text worked
                except:
                    print("no location")
                    location.append("no location")


                


                # scraped_data.append(list)

                # print("scraped_data for this page is: ")
                # # print(type(scraped_data)) #list
                # print(scraped_data)

            # print("scraped_data: ")
            # print(type(scraped_data)) #list
            # print(scraped_data)

            
            driver.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
            print("clicked")
            time.sleep(50)

        return ("success")
        print("collected data: ")
        print(type(scraped_data)) #list
        print(scraped_data)
        print("location list: ")
        print(type(location))
        print(location)
        print("First set: ")
        return(scraped_data[0])
        print(location[0])
        print(reviewtext_to_analyze)
            
        # return ('hohoho')

        sia = SIA()
        # print("ready data: ")
        # print(type(reviewtext_to_analyze))
        # print(reviewtext_to_analyze)
        analysis_result = []

        # First - sentiment analysis (positive/negative) on original review text
        review_rawtext = [x['reviewtextraw'] for x in scraped_data]
        print("testing is: ")
        # print(testing)

        for review in review_rawtext:
            pol_score = sia.polarity_scores(review)
            pol_score['reviewtext'] = review
            analysis_result.append(pol_score)

        # pprint(analysis_result, width = 200, compact = True)

        df = pd.DataFrame.from_records(analysis_result)
        df.head()
        print(df)

        df['label'] = 0
        df.loc[df['compound'] > 0.2, 'label'] = 1
        df.loc[(df['compound'] < -0.1) & (df['neg'] > 0.142), 'label'] = -1
        df.loc[(df['neu'] > 0.7) & (df['pos'] > 0.18) & (df['compound'] < 0.84), 'label'] = 0
        df.head()
        print(df)

        print(df.label.value_counts())
        print(df.label.value_counts(normalize=True) * 100)

        # #reviews with positive score only
        pos_lines_positive = df[df.label == 1].reviewtext
        print("priting positive reviews: ")
        print(pos_lines_positive)

        positive = []
        for i in pos_lines_positive:
            positive.append(i)

        print(positive)

        #reviews with negative score only
        pos_lines_negative = df[df.label == -1].reviewtext

        # print("type of pos_lines_positive: ")
        print(type(pos_lines_positive)) #list
        print("printing negative reviews:")
        print(pos_lines_negative)
        #reviews with neutral score only
        pos_lines_neutral = df[df.label == 0].reviewtext

        # print("type of pos_lines_positive: ")
        # print(type(pos_lines_positive)) #list
        print("printing neutral reviews:")
        print(pos_lines_neutral)

        #start text cleaning from here
        #positive reviews
        lowercase_nopunctuation = []
        removed_list_positive = []
        for review_text in pos_lines_positive:
            #lowercase and remove puncutations
            lowercase_nopunctuation = nltk.word_tokenize(review_text.lower())
            removed = [word for word in lowercase_nopunctuation if word.isalnum()]
            removed_list_positive.append(removed)

        #negative reviews
        lowercase_nopunctuation_negative = []
        removed_list_negative = []
        for review_text in pos_lines_negative:
            #lowercase and remove puncutations
            lowercase_nopunctuation_negative = nltk.word_tokenize(review_text.lower())
            removed = [word for word in lowercase_nopunctuation_negative if word.isalnum()]
            removed_list_negative.append(removed)

        print("lowercased and puncuations removed: ")
        print(len(removed_list_positive))
        print(len(removed_list_negative))
        

        #spelling correction  
        spelling_corrected_positive = []
        spelling_corrected_negative = []

        #spelling correction
        #positive
        for word in removed_list_positive:
            if word == "disney" or "hong" or "kong" or "hk": 
                spelling = ' '.join(word)
                spelling_corrected_positive.append(spelling)
            else:
                output = str(TextBlob(word).correct())
                spelling = ' '.join(output)
                spelling_corrected_positive.append(output)

        #negative
        for word in removed_list_negative:
            if word == "disney" or "hong" or "kong" or "hk": 
                spelling = ' '.join(word)
                spelling_corrected_negative.append(spelling)
            else:
                output = str(TextBlob(word).correct())
                spelling = ' '.join(output)
                spelling_corrected_negative.append(output)

        print("spelling corrected: ")
        print(spelling_corrected_positive) 

        #breaking down words by words
        stop_words = set(stopwords.words("english"))
        # positive 
        corrected_text_positive = ' '.join(spelling_corrected_positive)
        print("corrected_text_positive: ")
        print(corrected_text_positive)
        print(type(corrected_text_positive)) #str
        word_tokens_positive = word_tokenize(corrected_text_positive)

        # negative
        corrected_text_negative = ' '.join(spelling_corrected_negative)
        # print(corrected_text)
        #print(type(corrected_text)) #str
        word_tokens_negative = word_tokenize(corrected_text_negative)  

        # filtering and removing stop words
        # positive
        filtered_text_positive = [w for w in word_tokens_positive if not w in stop_words]

        # negative
        filtered_text_negative = [w for w in word_tokens_negative if not w in stop_words]
        print("filtered_text: ")
        # print(filtered_text)

        # positive
        pos_freq = nltk.FreqDist(filtered_text_positive)
        print("common words in positive reviews (only) are: ")
        print(type(pos_freq))
        print(pos_freq.most_common(20))

        # pos_lines_positive = df[df.label == 1].reviewtext

        common_words_positive = pos_freq.most_common(20)
        print(type(common_words_positive)) #list
        print(common_words_positive) #list of top 20 positive common words

        positive_top_words = []
        positive_top_words_freq = []
        for i in common_words_positive:
            word_text = i[0]
            # print(word_text)
            word_freq = i[1]
            positive_top_words.append(word_text)
            positive_top_words_freq.append(word_freq)

            
        
        print(positive_top_words)
        print(positive_top_words_freq)


        # negative
        pos_freq_negative = nltk.FreqDist(filtered_text_negative)
        print("common words in negative reviews are: ")
        print(pos_freq_negative.most_common(20))

        
        # return ("ohoho")
        return render_template("test2.html", search_string = search_string, location = location,
        positive=positive, positive_top_words=positive_top_words,
        positive_top_words_freq=positive_top_words_freq)
        return render_template("test.html", search_string = search_string)
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
