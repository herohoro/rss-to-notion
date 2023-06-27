import os
import time
import json
import requests
import feedparser
from dateutil import parser
from urllib.parse import urlparse
import sqlite3
from sqlite3 import Error
from dotenv import load_dotenv

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
                                    source text NOT NULL,
                                    title text NOT NULL,
                                    link text NOT NULL
                                ); """
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)

# RSSフィードのエントリをデータベースに追加します。
def add_content_to_db(conn, source, title, link):
    sql_check_article = """ SELECT * FROM articles WHERE source=? AND title=? AND link=? """
    cur = conn.cursor()
    cur.execute(sql_check_article, (source, title, link))
    rows = cur.fetchall()

    if len(rows) == 0: # この記事がまだデータベースに存在しない場合
        sql_insert_article = ''' INSERT INTO articles(source, title, link)
                                 VALUES(?,?,?) '''
        cur.execute(sql_insert_article, (source, title, link))
        conn.commit()
        return True
    else:
        print('This entry already exists.')
        return False

def addContent(source, title, date, link, conn):
    try:
        if add_content_to_db(conn, source, title, link):
            load_dotenv()

            # os.environ['TOKEN'] =''
            # os.environ['DATABASE_ID'] = ''

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

            response = requests.request("POST", notionUrl, headers=headers, data=data)
            print(response)
    except Exception as e:
        print(f"Error occurred while adding content to Notion: {e}")

def job(urls):
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        
        for url in urls:
            try:
                source = urlparse(url).netloc  # URLからホスト名を抽出します
                elements = feedparser.parse(url)


            
                for i, entry in enumerate(elements.entries):
                    # if i >= 10:  # 10件以上処理されたらループを抜けます
                    #     break

                    title = entry.title
                    date = entry.published
                    date = parser.parse(date).strftime('%Y-%m-%d %H:%M')
                    link  = entry.link       

                    addContent(source, title, date, link, conn)
                    time.sleep(1)
            except Exception as e:
                            print(f"Error occurred while parsing RSS feed from {url}: {e}")
            finally:
                conn.close()
    print("===== ❤(ӦｖӦ｡)さいごまで終わった〜 =====")  # プログラムが成功した時に表示されるメッセージ
## 登録したいRSSフィードのURLをここに入れてね
urls = ['https://ent.sbs.co.kr/news/xml/RSSFeed.do', 'https://learningenglish.voanews.com/api/zj-oqqeyviqq']
job(urls)

