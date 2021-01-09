# RateMe 
Inspired by the subreddit r/TrueRateMe. Upload your picture and get a rating of your face. 
Most people falls on the scale 4.5-5.5 (think of the normal curve)

## How it was built
I first built a webscraper to collect images from r/TrueRateMe, encoded them, and get the average rating. Then, I built a linear regression ML program to make a model and predict another set of data

On the front-end side of things, this site is built and served using *<placeholder - I haven't got to this part yet>*. It lets users upload their picture, that is later passed on to the server. 

## The Margin of Error
This program is still on a very early stage of development. That being said, there are many possible source of error that makes the prediction inaccurate. These are what I can think of at the top of my head
- The bot that analyses rating in the comment section doesn't do so intelligently. Instead, it retrieves the first numeric value and store it as a rating. For example, if a comment is
`I don't understand why people are giving you a 3.5. You're clearly a 4.2`,
the bot takes 3.5 as a rating instead of 4.2.
- There are way more data that lies within 4-6 scale, hence the program most likely to predict that you are within that range as well
- I honestly don't understand how machine learning works, so maybe linear regression is not the best method. This is something I'm still looking at..

# How to run the program in your own machine
- Make sure you have a python > 3.6.5
- Make sure you have pip3 installed
- Clone this repository
- Open your terminal, navigate to this folder
- (Optional) Create **and Activate** a virtual environment (see instruction for windows, linux or mac [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- Run `pip3 install -r requirements.txt`
- Run `python3 scraper.py` to run the webscraper
