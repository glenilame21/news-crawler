import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# simply uses username password to login to the website

login = 'https://energycharts.enerchase.de/'

form_data = {
    'Email-4': 'georg.isola@kelag.at',
    'Password-4': 'N8sLvbsB'
}

# login to the website, make a request to the page and get the html content
with requests.Session() as session:
        post = session.post(login, data=form_data, verify=False)
        request = 'https://energycharts.enerchase.de/energycharts/energycharts---flashlights'
        t = session.get(request, verify = False)
        html_content = t.text
        soup = BeautifulSoup(html_content, 'lxml')

# lists to store the data
main_titles = []
categories = []
dates = []
text = []


titles = soup.find_all('h2', class_='f-heading-detail-small')
for title in titles:
    main_titles.append(title.text)

# get the categories
category = soup.find_all('div', class_='fl_tag')
for i in category:
    categories.append(i.text)

# get the dates
date = soup.find_all('div', class_='date')
for i in date:
    dates.append(i.text)

# dates need to be converted to datetime objects

timestpamps = []
for i in dates:
    timestpamps.append(datetime.strptime(dates[-1], '%Y-%m-%d %I:%M %p'))

# get the body of the articles
body = soup.find_all('div', class_='w-richtext')
for i in body:
    text.append(i.text)


merged_data = []

for i in range(len(titles)):
    # Create a dictionary for the current item
    item = {
        'title': main_titles[i],
        'category': categories[i],
        'date': timestpamps[i],
        'body': text[i]
    }
    # Append the dictionary to the list
    merged_data.append(item)


download_path = 'C:/Users/z_lame/Desktop/Gleni Test/Download/Energy Charts/Flashlights'

titles_tracker_path = os.path.join(download_path, 'titles_tracker.json')

# Load existing titles tracker if it exists, otherwise initialize an empty set
try:
    with open(titles_tracker_path, 'r', encoding='utf-8') as file:
        titles_tracker = set(json.load(file))
except FileNotFoundError:
    titles_tracker = set()

for i, title in enumerate(main_titles):
    # Check if the title is already tracked to avoid scraping it again
    if title not in titles_tracker:
        # Add the title to the tracker
        titles_tracker.add(title)

        # Create a dictionary for the current article
        article_data = {
            'title': title,
            'category': categories[i],
            'date': dates[i], 
            'text': text[i]
        }

        # Sanitize title to create a valid filename
        filename = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filepath = os.path.join(download_path, f"{filename}.json")

        # Save the article data as a JSON file
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(article_data, file, indent=4, ensure_ascii=False)

# Save the updated titles tracker to a JSON file
with open(titles_tracker_path, 'w', encoding='utf-8') as file:
    json.dump(list(titles_tracker), file, indent=4, ensure_ascii=False)