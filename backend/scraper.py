# this class navigates through r/TrueRateMe
# parse HTML, put it in a json file

import re
import json 
import csv
import os
from typing import Union
from datetime import datetime
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from time import sleep
from face import get_features
from predictor import train
import numpy as np

url = 'https://www.reddit.com/r/truerateme/'

# step 1: find clickable div to see each post
class Crawler():
    def __init__(self):
        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 1 
        })
        self.driver = webdriver.Chrome(options=option)
    
    def get_data(self):
        # make a csv file to store data
        f = open('feature-data.csv', 'a+')
        writer = csv.writer(f)
        
        # click open each entry in the subreddit
        contents = self.driver.find_elements_by_css_selector('._1poyrkZ7g36PawDueRza-J._11R7M_VOgKO1RJyRSRErT3')
        for c in contents:
            try:
                c.click()
            except ElementNotInteractableException:
                print('image not interactable')
                continue

            data = {}
            images = self.driver.find_elements_by_css_selector('div._3Oa0THmZ3f5iZXAQ0hBJ0k > a > img')
            #if there is no images, go to other content
            if images == []:
                self.close_window()
                print('no image')
                continue

            # handle each image in entries
            index = 0
            for i in images:
                src = i.get_attribute('src')
                data[f'url{index}'] = src
                request = {
                    'image': {
                        'source': {
                            'image_uri': src
                            },
                        },
                    }
                face_features = get_features(request=request)
                data[f'features{index}'] = face_features
                index += 1
            
            # handle each comments in entry
            comments = self.driver.find_elements_by_class_name('_1qeIAgB0cPwnLhDF9XSiJM')
            if comments == []:
                self.close_window()
                continue
            count, average = self.analyse_comments(comments)

            # write to csv -> url, features, number of rating, average rating
            for i in range(0, index):
                if count != 0:
                    self.write_to_file(writer, data[f'url{i}'], data[f'features{i}'], count, average)
            self.close_window()
        f.close()


    # loop through all comments, get data, compute count of ratings & average rating
    def analyse_comments(self, comments: list) -> Union[int, float]:
        total_score = 0
        comments_with_score = 0

        for com in comments:
            text = com.get_attribute("textContent")
            # very long comments normally not a rating but
            # more of an advice
            if len(text) > 80:
                continue
            # skip links to simplify the code
            if 'http' in text.lower():
                continue
            if 'rule' in text.lower() or 'guide' in text.lower():
                continue

            dec_list = re.findall('\d+\.?\d*', text)
            if len(dec_list) == 0:
                continue

            d = 0
            for d in dec_list:
                # find the first instance of d that is between 0 and 10
                d = float(d)
                if d > 0 and d <= 10:
                    comments_with_score += 1
                    total_score += d
                    break
        
        if comments_with_score > 0:
            return comments_with_score, total_score/comments_with_score
        else:
            return 0, 0


    def write_to_file(self, writer, url: str, features: list, count: int, avg: float):
        #   date, image_url, features, count_rating, avg_rating
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        if url == '' or features == [] or count == 0 or avg == 0.0:
            return
        
        data = list()
        data += [date, url, count, avg]
        data += features
        writer.writerow(data)

    def close_window(self):
        try:
            btn = self.driver.find_element_by_css_selector('div._25ONQRwoX20oeRXFl_FZXt > button')
        except NoSuchElementException:
            pass
        else:
            btn.click()
        sleep(1)
    
            
crawler = Crawler()
crawler.driver.get(url)

#scroll to the bottom of the page
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = crawler.driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    crawler.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = crawler.driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

crawler.driver.execute_script("window.scrollTo(0, 0);")
crawler.get_data()
#train()