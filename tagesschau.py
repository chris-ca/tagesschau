#!/usr/bin/env python3
from config import cfg
import os
import requests
from diskcache import Cache
import jinja2
import simplemailer
cache = Cache(cfg['cache_path'])

@cache.memoize(expire=cfg['cache_duration'])
def hp_news():
    r = requests.get('https://www.tagesschau.de/api2/homepage/')
    contents = r.json()
    return contents['news']
news_entries = hp_news()

last_entry = news_entries[0]

templateLoader = jinja2.FileSystemLoader(searchpath=str(os.path.dirname(os.path.abspath(__file__))))
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "news.html"
template = templateEnv.get_template(TEMPLATE_FILE)
html = template.render(entries=news_entries)
simplemailer.SimpleSMTP.from_config() \
.subject('News update: {title} '.format(**last_entry)) \
.html(html) \
.send()
