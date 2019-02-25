from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import requests
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # visit NASA mars site

    url = 'https://mars.nasa.gov/news'
    html = browser.visit(url)

    time.sleep(1)

    # make martian soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #find the articles

    articles = soup.find('article').find('a')['href']
    articles_url = f'{url}{articles}'

    # Grab the first title
    newest_title = soup.find('article').find('a').find('h3').text

    # Go to the page with the text 
 
    html = browser.visit(articles_url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # lift the first paragraph
    newest_p = soup.article.find_all('p')
    newest_p = newest_p[1].text

    #Heading to the Rocket Lab for some pictures

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    html = browser.visit(jpl_url)

    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #head to the full images
    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(1)

    #grab the full image

    images = soup.find('body').find("img", class_="fancybox-image")["src"]
    featured_image_url = f'https://www.jpl.nasa.gov{images}'

    # Tweeting with InSight

    mars_url = 'https://twitter.com/marswxreport?lang=en'
    html = browser.visit(mars_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Grab the weather
    text=  soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    mars_weather = text.split('\n')[0]

    # Grab some Martian facts
    USGS_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(USGS_url)

  #  geo_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   # html = browser.visit(geo_url)

 #   html = browser.html
 #   soup = BeautifulSoup(html, 'html.parser')

#found = soup.find('div', class_="collapsible results").find_all('a')
#found_link = found[::1]
#geo_links = []
#for n in range(len(found_link)):
#    geo_links.append(found_link[n]['src'])

# soup.find('div', class_="collapsible results").find_all('a')
    mars_data = {
        "news_title" : newest_title,
        "news_p" : newest_p,
        "featured_image_url" : featured_image_url,
        "mars_weather" : mars_weather,
        'mars_table' : tables
    }
    browser.quit()

    return mars_data
