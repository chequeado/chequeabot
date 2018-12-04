import datetime

import newspaper
import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.minutouno.com'

class MinutoUnoSpider(scrapy.Spider):
    name = "m1"

    def start_requests(self):
        
        urls = [
            'https://www.minutouno.com/politica',
            'https://www.minutouno.com/economia'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        noticias = set(response.xpath('//div[@class="note"]/article//a[contains(@href,"notas")]/@href').extract())
        for noticia_url in noticias:
            yield scrapy.Request(url=noticia_url, callback=self.parse_noticia)


    def parse_noticia(self, response):

        ff = newspaper.Article(response.url)
        ff.download()
        ff.parse()
        noticia_fecha = ff.publish_date
        if not noticia_fecha:
            try:
                fecha_texto =  response.xpath('//span[@class="date"]/text()').extract()[0].split('-')[0].lower().strip()
                noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d de %B de %Y')
            except:
                noticia_fecha = datetime.datetime.now()

        noticia_cuerpo = ff.text

        data = {
            'titulo': ff.title,
            'fecha': noticia_fecha,
            'noticia_texto': noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'minuto1',
            'formato': 'web'
        }

        yield data
        
    
