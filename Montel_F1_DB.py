import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import json
import re
import sqlite3

# Function For Timestamp Retreival 
def timestamp(time_elements, dates, today):
    for i in time_elements:
        text = i.get_text().strip()
        if 'ago' in text:
            date = today
        else:
            try:
                date = datetime.strptime(text, '%d.%m.%Y %H:%M').date()
            except ValueError:
            # Handle the error or skip the date
                print(f"empty timestamp found: {text}")
                continue  # Skip this iteration
        dates.append(date)

# Function For Time And Date Retreival
def time_date(eletricity_topic_soup):
    time_elements = eletricity_topic_soup.find_all('time', class_='news-item__date')

    dates = []
    today = datetime.now().date()
    return time_elements,dates,today

# Function For Article Title Retreival
def article_title(eletricity_topic_soup, dates, today):
    article_title = eletricity_topic_soup.find_all('h2', class_='news-item__title')

    links = []

    for article in article_title:
      print(article.text.strip())

      todays_news_filtered = []

      for i in range(len(dates)):
        if dates[i] == today:  
            todays_news_filtered.append(article_title[i].text.strip())
    return article_title,links

# Function For Appending URL
def append_url(dates, today, article_title, links):
    base_url = 'https://montelnews.com'
    full_urls = []

    for i in range(len(dates)):
        if dates[i] == today:  
            links.append(article_title[i].find('a')['href']) 

    for link in links:
      full_urls.append(base_url + link)
    return full_urls

# Final File To Save

def scrape_and_save(url_list, directory):

    titles_file_path = os.path.join(directory, 'titles.json')
    
    # Step 1: Load existing titles
    try:
        with open(titles_file_path, 'r', encoding='utf-8') as file:
            existing_titles = json.load(file)
    except FileNotFoundError:
        existing_titles = []

    for url in url_list:
        response = requests.get(url, verify=False)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        try:
            title = soup.find('h1', class_='article__title').text.strip()
            title = re.sub(r'[\\/*?:"<>|]', "-", title)
            
            # Step 2: Check title before scraping
            if title in existing_titles:
                print(f"Skipping already scraped article: {title}")
                continue  # Skip this iteration
            
            existing_titles.append(title)  # Add new title to the list
        except Exception as e:
            print(f"Error retrieving title for URL {url}: {e}")
            continue  # Skip to the next URL if there's an error

        subtitle = soup.find('p', class_='article__lead').text.strip()
        body = soup.find('div', class_='article__body bard').text.strip()
        
        # Extract category from the URL
        category = []
        category_element = soup.find_all('a', class_='article__topic')
        for i in category_element:
            category.append(i.text.strip())

        category_json = json.dumps(category)
            

        df = pd.DataFrame({
            'title': [title],
            'subtitle': [subtitle],
            'body': [body],
            'datestamp': [datetime.now().strftime('%d-%m-%Y')],
            'category': [category]
        })
        try:
            #connect to db
            conn = sqlite3.connect('montel.db')
            c = conn.cursor()

            #create table
            c.execute('''CREATE TABLE IF NOT EXISTS montelwithtimestamp(
                      title TEXT PRIMARY KEY,
                      subtitle TEXT,
                      body TEXT,
                      datestamp TEXT,
                      category TEXT)''')
            
            #INSERT DATA
            c.execute('INSERT INTO montelwithtimestamp (title, subtitle, body, datestamp, category) VALUES (?,?,?,?,?)',
                      (title, subtitle, body, datetime.now().strftime('%d-%m-%Y'), category_json))
            
            #commit and close
            conn.commit()
            conn.close()
            print(f"Saved Article to Montel DB: {title}")

        except Exception as e:
            print(f"Error saving article to Montel DB: {e}")

        #save df to json
        json_str = df.to_json(orient='records', indent=4)
        json_file_path = os.path.join(directory, f'{title}.json')
        with open(json_file_path, 'w', encoding='utf-8') as file:
            file.write(json_str)

    # Step 3: Update and save titles
    with open(titles_file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_titles, file, indent=4)

