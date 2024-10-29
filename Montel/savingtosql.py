import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import json
import re
import sqlite3
import pyodbc


def db_scrape_and_save(url_list, directory):

    titles_file_path = os.path.join(directory, 'titles.json')

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=SQLBI01;'
                          'DATABASE=DH_SANDBOX;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    
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
            'category': [category],
            'source': 'Montel'
        })
        try:
           #INSERT DATA
            cursor.execute('INSERT INTO mercurius.Scraper (title, subtitle, body, date, category, source) VALUES (?,?,?,?,?,?)',
                (title, subtitle, body, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), category_json, 'Montel'))
            
            #commit and close
            conn.commit()
            conn.close()
            print(f"Saved Article to Scraper Table From Montel: {title}")

        except Exception as e:
            print(f"Error saving article from Montel: {e}")

        #save df to json
        json_str = df.to_json(orient='records', indent=4)
        json_file_path = os.path.join(directory, f'{title}.json')
        with open(json_file_path, 'w', encoding='utf-8') as file:
            file.write(json_str)

    # Step 3: Update and save titles
    with open(titles_file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_titles, file, indent=4)