from datetime import datetime
import locale
from time import mktime

import feedparser
import newspaper
import scrapy


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'https://www.clarin.com'

class ClarinSpider(scrapy.Spider):
    name = "clarin"

    def start_requests(self):
        urls = ["https://www.clarin.com/rss/politica/", "https://www.clarin.com/rss/economia/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        feed = feedparser.parse(response.url)
        for entry in feed['entries']:
            request = scrapy.Request(url=entry['link'], callback=self.parse_noticia)
            request.meta['item'] = entry           
            yield request


    def parse_noticia(self, response):
        ff = newspaper.Article(response.url)
        ff.download()
        ff.parse()
        texto = ff.text
        titulo = ff.title
        noticia_url = ff.url
        noticia_fecha = datetime.fromtimestamp(mktime(response.meta['item']['published_parsed']))
        
        data = {
            'titulo': titulo,
            'fecha': noticia_fecha,
            'noticia_texto': texto,
            'noticia_url': noticia_url,
            'source': 'clarin',
            'formato': 'web'
        }

        yield data
        
    