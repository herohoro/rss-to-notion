import feedparser
import requests, json
import os
import time
import datetime

def addContent(title, date, link):
    
    token = os.getenv('TOKEN')
    databaseId = os.getenv('DATABASE_ID')

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    notionUrl = 'https://api.notion.com/v1/pages'
    addData = {
        "parent": { "database_id": databaseId },
        "properties": {
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

    response = requests.request("POST", notionUrl, headers=headers, data=data)
    print(response)

url = 'https://www.happyou.info/fs/gen.php?u=2083537882&p=1344155542'

def job(url):
    elements = feedparser.parse(url)

    for entry in elements.entries:
        title = entry.title
        date = entry.published
        date = datetime.datetime.strptime(str(date), '%a, %d %b %Y %H:%M:%S +0000').strftime('%Y-%m-%d %H:%M')
        link  = entry.link       
        addContent(title, date, link)


        time.sleep(1)
        
job(url)
