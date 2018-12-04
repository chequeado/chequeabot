import datetime

import newspaper
import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'https://www.ellitoral.com.ar/'

class ElLitoralSpider(scrapy.Spider):
    name = "ellitoral"

    def start_requests(self):
        
        urls = [
            'https://www.ellitoral.com/index.php/um/politica'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        news = newspaper.build(response.url)
        noticias = news.articles
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
        noticia_fecha = ff.publish_date if ff.publish_date else datetime.datetime.now()

        data = {
            'titulo': titulo,
            'fecha': noticia_fecha,
            'noticia_texto': texto,
            'noticia_url': noticia_url,
            'source': 'El Litoral',
            'formato': 'web'
        }

        yield data