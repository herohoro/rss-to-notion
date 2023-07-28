import requests
from pprint import pprint
import os
import json
from dateutil import parser
from urllib.parse import urlparse
import feedparser
import time
from dotenv import load_dotenv

def get_feeds():
    load_dotenv()  # take environment variables from .env.

    NOTION_ACCESS_TOKEN = os.getenv("FEED_DB_ID")
    NOTION_DATABASE_ID = os.getenv("NOTION_FEED_ID")

    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
    'Authorization': 'Bearer ' + NOTION_ACCESS_TOKEN,
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json',
    }
    r = requests.post(url, headers=headers)
    data = r.json().get('results')
    contents = [i['properties'] for i in data]
    # If Enabled is True, get properties.URL.url from contents
    urls=[i['URL']['url'] for i in contents if i['Enable']['checkbox']==True]

    # pprint(urls)
    return urls

def addContent(source, title, date, link):
            load_dotenv()
            
            NOTION_ACCESS_TOKEN = os.getenv("NOTION_TOKEN")
            NOTION_DATABASE_ID = os.getenv("READ_DB_ID")

            headers = {
                "Authorization": "Bearer " + NOTION_ACCESS_TOKEN,
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            notionUrl = 'https://api.notion.com/v1/pages'
            addData = {
                "parent": { "database_id": NOTION_DATABASE_ID },
                "properties": {
                    "source": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": source
                                }
                            }
                        ]
                    },
                    "title": {
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    },
                    "date": {
                        "date": 
                            {
                                "start": date
                            }
                    },
                    "link" : {
                        "url": link
                    }
                }
            }
            
            data = json.dumps(addData)

            
            try:
                response = requests.request("POST", notionUrl, headers=headers, data=data, timeout=5)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
            else:
                pprint(response)
                #  print(NOTION_DATABASE_ID)
    
def parse_feeds(urls): 
    for url in urls:
        
        source = urlparse(url).netloc  # URLからホスト名を抽出します
        elements = feedparser.parse(url)

        for i, entry in enumerate(elements.entries):

            title = entry.title
            date = entry.published
            date = parser.parse(date).strftime('%Y-%m-%d %H:%M')
            link  = entry.link       

            addContent(source, title, date, link)
            # pprint({'source': source, 'title': title, 'date': date, 'link': link})

            time.sleep(1)


def job():
    urls = get_feeds()
    parse_feeds(urls)

if __name__ == "__main__":
    job()
    pprint("===== ❤(ӦｖӦ｡)さいごまで終わった〜 =====")  # プログラムが成功した時に表示されるメッセージ