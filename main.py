import os
import time
import json
import requests
import feedparser
import datetime
import sqlite3
from sqlite3 import Error

# データベース接続を作成します。
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('rss_feed.db') # 'rss_feed.db' という名前のSQLiteデータベースに接続します。
        print(sqlite3.version)
    except Error as e:
        print(e)
    if conn:
        return conn

# テーブルを作成します。
def create_table(conn):
    try:
        sql_create_table = """ CREATE TABLE IF NOT EXISTS articles (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    link text NOT NULL
                                ); """
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)

# RSSフィードのエントリをデータベースに追加します。
def add_content_to_db(conn, title, link):
    sql_check_article = """ SELECT * FROM articles WHERE title=? AND link=? """
    cur = conn.cursor()
    cur.execute(sql_check_article, (title, link))
    rows = cur.fetchall()

    if len(rows) == 0: # この記事がまだデータベースに存在しない場合
        sql_insert_article = ''' INSERT INTO articles(title,link)
                                 VALUES(?,?) '''
        cur.execute(sql_insert_article, (title, link))
        conn.commit()
        return True
    else:
        print('This entry already exists.')
        return False

def addContent(title, date, link, conn):
    if add_content_to_db(conn, title, link):

        os.environ['TOKEN'] =''
        os.environ['DATABASE_ID'] = ''

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

url = 'https://www.happyou.info/fs/gen.php?u=2083537882&p=-437531470'

def job(url):
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        elements = feedparser.parse(url)

        for entry in elements.entries:
            title = entry.title
            date = entry.published
            date = datetime.datetime.strptime(str(date), '%a, %d %b %Y %H:%M:%S +0000').strftime('%Y-%m-%d %H:%M')
            link  = entry.link       
            addContent(title, date, link, conn)
            time.sleep(1)

        conn.close()
        
job(url)

