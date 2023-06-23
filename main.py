import feedparser
import requests, json
import os
import time
import datetime

def addContent(title, date, link):
    
    token = os.getenv('TOKEN')
    # I want to use databaseId from .env file
    # databaseId = os.getenv('DATABASE_ID')
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
        # sample is Fri, 23 Jun 2023 11:45:00 GMT
        # but I want Mon, 27 Mar 2023 00:00:00 +0000

        # strptimeで文字列をdatetime型に変換
        # strptime(文字列, フォーマット) → strftime(フォーマット)
        # フォーマット → https://docs.python.org/ja/3/library/datetime.html#strftime-and-strptime-format-codes
        # Mon is format code %a
        # day is format code %d
        # %Z is timezone
        # +0000 is timezone
        # What difference between %Z and +0000?
        # %Z is timezone name
        # +0000 is timezone offset
        
        date = datetime.datetime.strptime(str(date), '%a, %d %b %Y %H:%M:%S +0000').strftime('%Y-%m-%d %H:%M')
        link  = entry.link       
        addContent(title, date, link)


        time.sleep(1)
        
job(url)
