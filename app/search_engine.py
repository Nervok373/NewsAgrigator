from datetime import datetime
import time

import requests
from bs4 import BeautifulSoup
import urllib3
from dataclasses import dataclass, asdict

from duckduckgo_search import DDGS
from . data_client import PostgresClient

urllib3.disable_warnings()  # отключает предуприждение о не безопасном потключении http

headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}


@dataclass
class News:
    source: str
    title: str
    author: str
    count_comments: str
    news_id: str
    score: str
    link: str
    description: str
    date_time: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


def google_api(query):
    API = "AIzaSyAOGY0T2mtMAkZ1Ju_JvAF7GjvUktnUg1g"
    SX = "553a06226cb5a499f"
    try:
        _url = f"https://www.googleapis.com/customsearch/v1?key={API}&cx={SX}&q={query}"
        _response = requests.get(_url)
        _response = _response.json()

        _out_data = []
        print(_response)
        for site in _response['items']:
            _out_data.append(
                {
                    'title': site['title'],
                    'link': site['link'],
                    'displayLink': site['displayLink'],
                    'snippet': site['snippet'],
                    'formattedUrl': site['formattedUrl']
            })

        return _out_data

    except Exception as e:
        print(e)


def duck_duck_go(query):
    try:
        _response = []
        with DDGS() as ddgs:
            for r in ddgs.text(keywords=query, region='ru-ru', safesearch='off', timelimit='y', max_results=10):
                _response.append({
                    "source": "DDG",
                    "title": r['title'],
                    "link": r['href'],
                    "snippet": r['body']
                })

        return _response

    except Exception as e:
        print(e)


def it_news_habr():
    urls = ['https://habr.com/ru/feed/'] + [f'https://habr.com/ru/feed/page{n}' for n in range(2, 10)]
    req_text = []

    for url in urls:
        time.sleep(2)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        post_urls = soup.findAll("div", class_="tm-article-snippet tm-article-snippet")

        try:
            for i in range(len(post_urls) - 1):
                news = News(
                    source="Habr",
                    title=post_urls[i].find('a', class_='tm-title__link').getText(),
                    author=str(post_urls[i].find('a', class_='tm-user-info__username').getText()
                                     ).replace('\n', '').replace(' ', ''),
                    count_comments="",
                    news_id="",
                    score="",
                    link=f"https://habr.com{post_urls[i].find('a', class_='tm-article-snippet__readmore').get('href')}",
                    description=(post_urls[i].find('div',
                                                    class_='article-formatted-body article-formatted-body '
                                                           'article-formatted-body_version-2').getText())[
                                 :750],
                    date_time=post_urls[i].find('time').get("title")
                )

                req_text.append(news.dict())


        except Exception as e:
            print(e, url)

    return req_text


def it_news_ycombin():
    top_stories_id_url = "https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"
    top_stories_id = requests.get(top_stories_id_url, headers=headers)
    stories_id = top_stories_id.text

    stories_id = (stories_id.replace(" ", "")
                  .replace("[", "").replace("]", "").
                  replace("\n", "")).split(",")

    data = []
    for id in stories_id[:30]:
        _url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty"
        response = requests.get(_url)
        story = response.json()

        news = News(
            source="Hacker News",
            title=story["title"],
            author=story["by"],
            count_comments=story["descendants"],
            news_id=story["id"],
            score=story["score"],
            link=story["url"],
            description="",
            date_time=datetime.utcfromtimestamp(story["time"]).strftime('%Y-%m-%d, %H:%M')
        )

        data.append(news.dict())

    return data


def create_db():
    data1 = it_news_habr()
    data2 = it_news_ycombin()

    data_client_imp = PostgresClient()
    conn = data_client_imp.get_connection()
    data_client_imp.create_table(conn, """
            CREATE TABLE IF NOT EXISTS app_news
        (
            id serial PRIMARY KEY,
            title text,
            author text,
            count_comments text,
            news_id text,
            score text,
            source text,
            time text,
            description text,
            link text
        )
    """)
    try:
        for item in data1:
            req = data_client_imp.insert(conn, f"""
            INSERT INTO app_news (title, author, count_comments, news_id, score,
            source, time, description, link) 
            VALUES ('{str(item["title"]).replace("'", "")}', '{item["author"]}', '{item["count_comments"]}',
             '{item["news_id"]}', '{item["score"]}', '{item["source"]}',
              '{item["date_time"]}', '{str(item["description"]).replace("'", "")}', '{item["link"]}')
            """)

    except Exception as e:
        print(e, item)

    try:
        for item in data2:
            req = data_client_imp.insert(conn, f"""
            INSERT INTO app_news (title, author, count_comments, news_id, score,
            source, time, description, link) 
            VALUES ('{str(item["title"]).replace("'", "")}', '{item["author"]}', '{item["count_comments"]}',
             '{item["news_id"]}', '{item["score"]}', '{item["source"]}',
              '{item["date_time"]}', '{str(item["description"]).replace("'", "")}', '{item["link"]}')
            """)

    except Exception as e:
        print(e, item)

    conn.close()


# create_db()
