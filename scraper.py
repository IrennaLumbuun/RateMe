# this class navigates through r/TrueRateMe
# parse HTML, put it in a json file

import os
import json 
import requests # to sent GET requests
from bs4 import BeautifulSoup # to parse HTML
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

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
        self.driver = webdriver.Chrome(chrome_options=option)
    
    def get_data(self):
        self.driver.get('https://www.reddit.com/r/truerateme/')
        contents = self.driver.find_elements_by_css_selector('._1poyrkZ7g36PawDueRza-J._11R7M_VOgKO1RJyRSRErT3')
        for c in contents:
            c.click()
            images = self.driver.find_elements_by_css_selector('div._3Oa0THmZ3f5iZXAQ0hBJ0k > a > img')
            # TODO: continue saving all images
            for i in images:
                src = i.get_attribute('src')
                print(src)
            
            # if there is "view entire discussion" button, click on it
            # TODO: try catch
            view_all = self.driver.find_element_by_xpath('//*[@id="overlayScrollContainer"]/div[2]/div[1]/div[2]/div[4]/div/button')
            comments = self.driver.find_elements_by_class_name('_1qeIAgB0cPwnLhDF9XSiJM')
            for com in comments:
                #TODO: analyse comments, get numbers
                text = com.get_attribute("innerHTML")
                print(text)
            
            # close window
            btn = self.driver.find_element_by_css_selector('div._25ONQRwoX20oeRXFl_FZXt > button')
            btn.click()
            sleep(1)
            
crawler = Crawler()
crawler.get_data()
'''
response = requests.get(url) # contains web content

soup = BeautifulSoup(response.content, "html.parser")
print(soup.prettify())

images = soup.find_all("img", attrs={"alt": "Post image"})

number = 0
for image in images:
    image_src = image["src"]
    print(image_src)
    # urllib.request.urlretrieve(image_src) this downloads each image
    number += 1
'''