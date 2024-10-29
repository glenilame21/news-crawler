import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import json
import re
from IEA_F import get_titles, get_url, scrape_and_save


#PROCESS THE URL AND MAKE THE SOUP
url = 'https://www.iea.org/news/'
<<<<<<< HEAD
IEA = requests.get(url)
=======
IEA = requests.get(url, verify=False)
>>>>>>> 0ccd8ff1bb7652e5d12956cfd52fc1f95ee596ee
IEA_soup = BeautifulSoup(IEA.text, 'html.parser')

#GET TITLES
get_titles(IEA_soup)

#GET LINKS
get_url(IEA_soup)


# SCRAPER & SAVE
<<<<<<< HEAD
scrape_and_save(get_url(IEA_soup), "C:/Users/Z_LAME/Desktop/Crawler/Downloads/News IEA")
=======
scrape_and_save(get_url(IEA_soup), "C:/Users/z_lame/Desktop/Gleni Test/Download/IEA/")

>>>>>>> 0ccd8ff1bb7652e5d12956cfd52fc1f95ee596ee
