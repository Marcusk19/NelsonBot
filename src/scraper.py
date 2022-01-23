# TODO
import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.reddit.com/r/NCSU/new/')

# print(r.status_code)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
# Getting the title
# print(soup.title)

