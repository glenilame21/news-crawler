import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

login = 'https://energycharts.enerchase.de/'
form_data = {
    'Email-4': 'georg.isola@kelag.at',
    'Password-4': 'N8sLvbsB'
}


with requests.Session() as session:
    post = session.post(login, data=form_data, verify=False)
    request = 'https://energycharts.enerchase.de/energycharts/energycharts---co2-marktbericht'
    t = session.get(request, verify = False)
    html_content = t.text
    soup = BeautifulSoup(html_content, 'lxml')


main_div = soup.find_all('div', class_='co2_richttext w-richtext')
timestamp = soup.find_all('div', class_='date marktbericht')
h3 = soup.find_all('h3', class_='co2_heading')

titles = []
timestamps = []
body = []

for i in main_div:
    body.append(i.text)

for i in h3:
    titles.append(i.text)

for i in timestamp:
    timestamps.append(i.text)

date_format = '%Y-%m-%d %I:%M %p'

dates = []

for i in timestamps:
    date = datetime.strptime(i, date_format)
    dates.append(date)

merged_data = []

for i in range(len(titles)):
    # Corrected 'timestpamps' to 'timestamps'
    item = {
        'title': titles[i],
        'date': dates[i],  # Assuming 'timestamps' is the correct list name
        'body': body[i]
    }
    merged_data.append(item)

download_path = 'C:/Users/z_lame/Desktop/Gleni Test/Download/Energy Charts/CO2'
titles_tracker_path = os.path.join(download_path, 'titles_tracker.json')

try:
    with open(titles_tracker_path, 'r', encoding='utf-8') as file:
        titles_tracker = set(json.load(file))
except FileNotFoundError:
    titles_tracker = set()

for i, title in enumerate(titles):
    if title not in titles_tracker:
        titles_tracker.add(title)

        article_data = {
            'title': title,
            'date': dates[i], 
            'text': body[i]
        }

        filename = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filepath = os.path.join(download_path, f"{filename}.json")

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(article_data, file, indent=4, default=str, ensure_ascii=False)

with open(titles_tracker_path, 'w', encoding='utf-8') as file:
    json.dump(list(titles_tracker), file, indent=4, default=str , ensure_ascii=False)