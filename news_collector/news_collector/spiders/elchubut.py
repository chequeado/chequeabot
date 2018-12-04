import datetime

import feedparser
import newspaper
import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.elchubut.com.ar/'

class ElChubutSpider(scrapy.Spider):
    name = "elchubut"

    def start_requests(self):
        
        urls = [
            'http://www.elchubut.com.ar/rss'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        feed = feedparser.parse(response.url)
        for entry in feed['entries']:
            if entry['category'] == 'Regionales':
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
        noticia_fecha = ff.publish_date if ff.publish_date else datetime.datetime.now()

        data = {
            'titulo': titulo,
            'fecha': noticia_fecha,
            'noticia_texto': texto,
            'noticia_url': response.url,
            'source': 'El Chubut',
            'formato': 'web'
        }

        yield data
        
    
