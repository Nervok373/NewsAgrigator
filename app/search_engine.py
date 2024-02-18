import requests
import urllib3
from dataclasses import dataclass, asdict

from duckduckgo_search import DDGS

urllib3.disable_warnings()  # отключает предуприждение о не безопасном потключении http


def google_api(query):
    API = "AIzaSyAOGY0T2mtMAkZ1Ju_JvAF7GjvUktnUg1g"
    SX = "553a06226cb5a499f"
    try:
        _url = f"https://www.googleapis.com/customsearch/v1?key={API}&cx={SX}&q={query}"
        _response = requests.get(_url)
        _response = _response.json()

        _out_data = []

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
        return e


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
        return e
