from flask import Flask, render_template, request
import requests
from forms import UrlSearchForm

import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui

import nltk
# nltk.data.path.append('TA_REVIEW_ANALYZER/nltk_data')

nltk.download("punkt")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem import PorterStemmer
ps = PorterStemmer()


from textblob import TextBlob
# from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA
from pprint import pprint
import pandas as pd
import numpy as np
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--proxy-server="direct://"')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')

# for LOCAL HOST comment out for deployment
driver_path = r'C:/Users/USER/chromedriver.exe'

# for heroku deployment
#driver_path = '/app/.chromedriver/bin/chromedriver'

driver= webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
driver.implicitly_wait(10)



app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():

    errors = []
    urlsearch = UrlSearchForm(request.form)
    search_string = urlsearch.data['search']

    if request.method == "POST":
    
        
        try:

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
        # driver.get(search_string)
        # print("getting")
        scraped_data = []
        location = []

        # return (search_string)

        reviewtext_to_analyze = []
        data_for_commonwords = []
        title_list = []
        reviewtext_raw_list = []
        reviewtext_list = []
        list = {}


        print("TEST")
        driver.implicitly_wait(10)
        # wait = ui.WebDriverWait(driver, 10)
        print("load")
        print(search_string)
        driver.get(search_string)

        for i in range (0, 10):

            for _ in range(2):   #try up to 2 times
                try:
                    time.sleep(10)
                    wait = ui.WebDriverWait(driver, 20)
                    print("GETTING PAGE")
                    
                    # show_more = wait.until(lambda driver: driver.
                    # element_to_be_clickable("_36B4Vw6t"))
                    # driver.execute_script("arguments[0].click();", show_more)
                    # print("clicked")
    
                    read_more = driver.find_element_by_class_name("_36B4Vw6t")
                    print("found read_more")
                    # read_more.click()   use excute_script below instead
                    driver.execute_script("arguments[0].click();", read_more)
                    print("read_more clicked")
                    
                    container = driver.find_element_by_class_name('_1c8_1ITO')
                    # print(container.text)
                    # for review_box in container:
                    #     print(type(review_box))

                    print(type(container))  #webelement
                   
                    title = container.find_elements_by_xpath('//div[@class="DrjyGw-P _1SRa-qNz _19gl_zL- _1z-B2F-n _2AAjjcx8"]/span')
                    
                    for a in title:
                        # list.update(reviewtitle = a.text)
                        # list['reviewtitle'] = a.text
                        print(a.text)
                        title_text = a.text
                        title_list.append(title_text)
                            
                    list['reviewtitle'] = title_list
    
                        
                    reviewtext = container.find_elements_by_xpath('//div[@class="DrjyGw-P _26S7gyB4 _2nPM5Opx"]/span')

                    print("REVIEW TEXT")

                    print(type(reviewtext))
                    for a in reviewtext:
                        print("THIS IS REVIEW TEXT")
                        reviewtext_raw = a.text
                        reviewtext_raw_list.append(reviewtext_raw)

                        
                        lowercase_text = a.text.lower()
                        
                        # removing punctuations
                        text_punctuations = nltk.word_tokenize(lowercase_text)
                        punctuations_removed = [word for word in text_punctuations if word.isalnum()]

                        reviewtext_list.append(punctuations_removed)

                        print("punctuations removed: ")
                        # print(punctuations_removed)

                        spelling_corrected = []

                        #spelling correction
                        for word in punctuations_removed:
                            if word == "disney" or "hong" or "kong" or "hk": 
                                spelling_corrected.append(word)
                            else:
                                output = str(TextBlob(word).correct())
                                spelling_corrected.append(word)

                        print("spelling_corrected: ")
                        print(type(spelling_corrected))

                        #breaking down words by words
                        stop_words = set(stopwords.words("english"))
    
                        word_tokens = word_tokenize(lowercase_text)
                        corrected_text = ' '.join(spelling_corrected)
                        
                        word_tokens = word_tokenize(corrected_text)
                        # print(word_tokens)

                        # filtering and removing stop words
                        filtered_text = [w for w in word_tokens if not w in stop_words]
                        # print(filtered_text)

                        #removing stop words and stemming
                        stemmed = []
                        
                        for w in word_tokens:
                            if w not in stop_words:
                                
                                filtered_text.append(w)
                                stemmed_text = ps.stem(w)
                                stemmed.append(stemmed_text)

                            
                        print("stop words removed for commonword analysis: ")
                        # print(filtered_text)
                        data_for_commonwords.append(filtered_text)

            
                        stemmed_text = ' '.join(stemmed)
                        # print("stemmed: ")
                        # print(stemmed_text)
                        
                        reviewtext_to_analyze.append(stemmed_text)

                    list['reviewtextraw'] = reviewtext_raw_list
                    list['reviewtext'] = reviewtext_list
                    scraped_data.append(list)
                        
                    # reviewer_location = container.find_elements_by_xpath('//div[@class="DrjyGw-P _26S7gyB4 NGv7A1lw _2yS548m8 _2cnjB3re _1TAWSgm1 _1Z1zA2gh _2-K8UW3T _1dimhEoy"]/span')
            
                    # print("REVIEWER LOCATION")

            
                    # print(type(reviewer_location))  #list 
                    # print(reviewer_location)
                    # # for a in reviewer_location:
                    # #     print(a.text)

                except Exception as e:  #if error
                    print("Error - please reload the page and try again")
                    time.sleep(2)
                else: 
                    # get out of the loop if no error  
                    break
            else:
                # if all 3 attemps fail
                driver.quit()
                return ("ERROR please try again")

            # driver.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
            driver.find_element_by_xpath('//div[@class="_1I73Kb0a"]').click()
            print("NEXT PAGE clicked")
            # return ("success") worked
            time.sleep(15)
        
        print("DATA DATA DATA")
        # print(scraped_data)
        print(type(scraped_data)) #list
        
        sia = SIA()
        # print("ready data: ")
        # print(type(reviewtext_to_analyze))
        # print(reviewtext_to_analyze)
        analysis_result = []

        # First - sentiment analysis (positive/negative) on original review text
        review_rawtext = [x['reviewtextraw'] for x in scraped_data]
        
        for review in reviewtext_raw_list:
            # print("test going")
            pol_score = sia.polarity_scores(review)
            pol_score['reviewtext'] = review
            analysis_result.append(pol_score)

        pprint(analysis_result, width = 200, compact = True)

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
        no_of_positivereviews = len(pos_lines_positive)
        print(pos_lines_positive)

        positive = []
        for i in pos_lines_positive:
            positive.append(i)

        # print(positive)
        positive_samples = positive[0:5]
        print(positive_samples)

        #reviews with negative score only
        pos_lines_negative = df[df.label == -1].reviewtext

        print(type(pos_lines_negative)) # pandas series
        print("printing negative reviews:")
        no_of_negativereviews = len(pos_lines_negative)
        print("number of negative reviews")
        print(no_of_negativereviews)

        negative = []

        if no_of_negativereviews == 0:
            negative.append("No negative reviews were found in the latest 100 reviews for the attraction.")
        else:
            for i in pos_lines_negative:
                print(i)
                negative.append(i)


        # print(negative)
        negative_samples = negative[0:5]
        print("NEGATIVE REVIEW:")
        print(negative_samples)

        #reviews with neutral score only
        pos_lines_neutral = df[df.label == 0].reviewtext

        # print(type(pos_lines_positive)) #list
        print("printing neutral reviews:")
        # print(pos_lines_neutral)

        

        # Second - start text cleaning 
        
        #positive reviews
        removed_list_positive = []

        print(type(pos_lines_positive))  #pandas series

        list_pos_lines_positive= pos_lines_positive.tolist()
        print(type(list_pos_lines_positive)) #list

        for i in list_pos_lines_positive:
            print(i)
            #lowercase and remove puncutations
            review_text_lowercase = i.lower()
            
            lowercase_nopunctuation = nltk.word_tokenize(review_text_lowercase)
            print(lowercase_nopunctuation)
            removed = [word for word in lowercase_nopunctuation if word.isalnum()]
            print(removed)
            removed_list_positive.append(removed)

        print("worked")
        #negative reviews
        lowercase_nopunctuation_negative = []
        removed_list_negative = []

        for text in pos_lines_negative:
            #lowercase and remove puncutations
            review_text_lowercase = text.lower()
            lowercase_nopunctuation_negative = nltk.word_tokenize(review_text_lowercase)
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
        

        # positive
        pos_freq = nltk.FreqDist(filtered_text_positive)
        print("common words in positive reviews (only) are: ")
        print(type(pos_freq))
        print(pos_freq.most_common(20))

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

        common_words_negative = pos_freq_negative.most_common(10)
        print(type(common_words_negative)) #list
        print(common_words_negative) #list of top 20 positive common words

        negative_top_words = []
        negative_top_words_freq = []

        if len(common_words_negative) == 0:
            negative_top_words.append("No negative reviews were found in the latest 100 reviews for the attraction")
            # negative_top_words_freq.append("No negative reviews were found in the latest 100 reviews for the attraction.")
        else:
            for i in common_words_negative:
                word_text = i[0]
                # print(word_text)
                word_freq = i[1]
                negative_top_words.append(word_text)
                negative_top_words_freq.append(word_freq)

        print(negative_top_words)
        print(negative_top_words_freq)

        
        # return ("data ready for results")
        return render_template("results.html", search_string = search_string, 
        positive=positive, 
        positive_samples=positive_samples,
        negative_samples=negative_samples,
        positive_top_words=positive_top_words,
        positive_top_words_freq=positive_top_words_freq,
        negative_top_words=negative_top_words,
        negative_top_words_freq=negative_top_words_freq,
        no_of_positivereviews=no_of_positivereviews,
        no_of_negativereviews=no_of_negativereviews)
        

    except:
        return ("Error - please reload the page and try again")
    finally:
        driver.quit()

    

if __name__ == '__main__':
      app.run()