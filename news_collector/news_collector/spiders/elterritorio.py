import datetime

import newspaper
import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.elterritorio.com.ar/'

class ElTerritorioSpider(scrapy.Spider):
    name = "elterritorio"

    def start_requests(self):
        
        urls = [
            'https://www.elterritorio.com.ar/misiones-1-seccion',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        el_territorio = newspaper.build('https://www.elterritorio.com.ar/misiones-1-seccion')
        noticias = el_territorio.articles
        for noticia in noticias:
            request = scrapy.Request(url=noticia.url, callback=self.parse_noticia)
            yield request


    def parse_noticia(self, response):
        ff = newspaper.Article(response.url)
        ff.download()
        ff.parse()
        texto = ff.text
        titulo = ff.title
        noticia_url = ff.url
        noticia_fecha = datetime.datetime.now()

        data = {
            'titulo': titulo,
            'fecha': noticia_fecha,
            'noticia_texto': texto,
            'noticia_url': noticia_url,
            'source': 'elterritorio',
            'formato': 'web'
        }

        yield data
        
    
