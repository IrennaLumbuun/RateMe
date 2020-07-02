# this class navigates through r/TrueRateMe
# parse HTML, put it in a json file

import os
import re
import json 
import requests # to sent GET requests
from bs4 import BeautifulSoup # to parse HTML
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from face import get_face

url = 'https://www.reddit.com/r/truerateme/'

# TODO:
# click on the clickable div
# get picture link
# get each comments
# save all in a json

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
        contents = self.driver.find_elements_by_css_selector('._1poyrkZ7g36PawDueRza-J._11R7M_VOgKO1RJyRSRErT3')
        for c in contents:
            c.click()
            
            images = self.driver.find_elements_by_css_selector('div._3Oa0THmZ3f5iZXAQ0hBJ0k > a > img')
            
            #if there is no images, go to other content
            if images == []:
                self.close_window()
                continue

            # TODO: continue saving all images
            for i in images:
                src = i.get_attribute('src')
                encoding = get_face(src)
                print(encoding)
            
            comments = self.driver.find_elements_by_class_name('_1qeIAgB0cPwnLhDF9XSiJM')

            if comments == []:
                self.close_window()
                continue
            self.analyse_comments(comments)
            self.close_window()


    def analyse_comments(self, comments: list):
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
                print('http')
                continue
            if 'rule' in text.lower() or 'guide' in text.lower():
                print('rule')
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
            print(f'count: {comments_with_score}')
            print(f'average = {total_score / comments_with_score}')


    def close_window(self):
        try:
            btn = self.driver.find_element_by_css_selector('div._25ONQRwoX20oeRXFl_FZXt > button')
        except NoSuchElementException:
            pass
        else:
            btn.click()
        sleep(1)
    
            
crawler = Crawler()
crawler.driver.get('https://www.reddit.com/r/truerateme/')

''' uncomment when not on testing mode
for loop in range(0, 50):
    # wait for it to load
    print('scrolling...')
    # Scroll down so Selenium can parse more stuffs
    crawler.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#go back to the top of the page
crawler.driver.execute_script("window.scrollTo(0, 0);")
'''

crawler.get_data()
