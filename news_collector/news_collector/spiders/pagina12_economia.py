from datetime import datetime

import newspaper
import scrapy

import locale

config = newspaper.Config()
config.browser_user_agent = 'Mozilla/5.0'
locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'https://www.pagina12.com.ar/'

class PaginaEcoSpider(scrapy.Spider):
    name = "p12_eco"

    def start_requests(self):
        
        urls = ['https://www.pagina12.com.ar/secciones/economia']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        links = set([e for e in response.xpath('//div[@id="list-container"]//a/@href')])
        for link in links:
            entry_url = response.urljoin(link.extract())
            request = scrapy.Request(url=entry_url, callback=self.parse_noticia)
            yield request


    def parse_noticia(self, response):
        ff = newspaper.Article(response.url, config)
        ff.download()
        ff.parse()
        texto = ff.text
        titulo = ff.title
        noticia_url = ff.url
        noticia_fecha = ff.publish_date if ff.publish_date else datetime.now()
        
        data = {
            'titulo': titulo,
            'fecha': noticia_fecha,
            'noticia_texto': texto,
            'noticia_url': noticia_url,
            'source': 'pagina12',
            'formato': 'web'
        }

        yield data
        
    
