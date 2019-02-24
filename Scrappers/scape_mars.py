from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import requests

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://mars.nasa.gov/news'
html = browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

articles = soup.find('article').find('a')['href']
articles

newest_title = soup.find('article').find('a').find('h3').text
newest_title

browser.click_link_by_partial_href(articles)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')
newest_p = soup.article.find_all('p')
newest_p = newest_p[1].text

newest_p

jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
html = browser.visit(jpl_url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

browser.click_link_by_partial_text('FULL IMAGE')

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

images = soup.find('body').find("img", class_="fancybox-image")["src"]

featured_image_url = f'https://www.jpl.nasa.gov{images}'
mars_url = 'https://twitter.com/marswxreport?lang=en'
html = browser.visit(mars_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')
text=  soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
mars_weather = text.split('\n')[0]

USGS_url = 'https://space-facts.com/mars/'
tables = pd.read_html(USGS_url)

jpl_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
html = browser.visit(jpl_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

found = soup.find('div', class_="collapsible results").find_all('a')
found_link = found[::1]
geo_links = []
for n in range(len(found_link)):
    geo_links.append(found_link[n]['src'])

 soup.find('div', class_="collapsible results").find_all('a')
