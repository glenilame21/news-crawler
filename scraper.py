import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import json
from Montel_F1_DB import timestamp , article_title , append_url , scrape_and_save,  time_date
import urllib3

# just to suppress the warning of SSL certificate verification - VERY ANNOYING WHEN WORKING UNDER KELAG NETWORK
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


urls = [
    'https://montelnews.com/topics/appointments',
    'https://montelnews.com/topics/storage',
    'https://montelnews.com/topics/biomass',
    'https://montelnews.com/topics/carbon',
    'https://montelnews.com/topics/coal',
    'https://montelnews.com/topics/consumption',
    'https://montelnews.com/topics/electricity',
    'https://montelnews.com/topics/results',
    'https://montelnews.com/topics/freight',
    'https://montelnews.com/topics/gas',
    'https://montelnews.com/topics/go',
    'https://montelnews.com/topics/hydrogen',
    'https://montelnews.com/topics/hydropower',
    'https://montelnews.com/topics/lignite',
    'https://montelnews.com/topics/lng',
    'https://montelnews.com/topics/nuclear',
    'https://montelnews.com/topics/offshore-wind',
    'https://montelnews.com/topics/oil',
    'https://montelnews.com/topics/policy',
    'https://montelnews.com/topics/ppa',
    'https://montelnews.com/topics/remit',
    'https://montelnews.com/topics/renewables'
    'https://montelnews.com/topics/smr',
    'https://montelnews.com/topics/solar',
    'https://montelnews.com/topics/trading',
    'https://montelnews.com/topics/transmission',
    'https://montelnews.com/topics/weather',
    'https://montelnews.com/topics/wind'
]


for url in urls:
    # REQUESTING THE URL
    eletricity_html = requests.get(url, verify=False)
    # PARSING THE HTML VIA BEAUTIFULSOUP
    eletricity_topic_soup = BeautifulSoup(eletricity_html.text, 'html.parser')

    # FUNCTION CALLS
    # Function For Time And Date Retreival
    time_elements, dates, today = time_date(eletricity_topic_soup)
    # Function For Timestamp Title Retreival
    timestamp(time_elements, dates, today)
    # Function For Filtered Title Retreival
    titles, links = article_title(eletricity_topic_soup, dates, today)
    # Function For Appending URLs
    full_urls = append_url(dates, today, titles, links)
    # Function For Scraping And Saving
    scrape_and_save(full_urls, "C:/Users/z_lame/Desktop/Gleni Test/Download/Montel/")