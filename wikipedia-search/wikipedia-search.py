# This is a simple webscraper to scrap summary of any topic from
# "https://en.wikipedia.org"
#
# Assumptions :
# 1. The search is well-formed i.e. it can be searched directly searched in
#    wikipedia
#    eg. 'harvard university' will work
# 2. Firefox is installed

# importing modules
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

# setting up a headless browser
options = Options()
options.set_headless(headless = True)

# opening site in web browser
browser = webdriver.Firefox(firefox_options = options)
browser.get('https://en.wikipedia.org')

# searching in seach box
elem = browser.find_element_by_name('search')
elem.send_keys('harvard university' + Keys.RETURN)   # make it more generalised

# to handle loading of new pages in selenium
# through the method of checking staleness of page
timeout = 30
old_page = browser.find_element_by_tag_name('html')
WebDriverWait(browser, timeout).until(staleness_of(old_page))

# getting the url of the new page
url = browser.current_url

# opening a socket and ignoring proxies
session = requests.Session()
session.trust_env = False
source = session.get(url)

# reading the data in a variable
html = source.text
soup = BeautifulSoup(html, 'html.parser')

# finding the appropriate section and printing
paras = soup.find_all('p')
req_para = paras[0]
print(req_para.text)
browser.close()
