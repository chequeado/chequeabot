import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'https://www.lacapital.com.ar/'

class LaCapitalSpider(scrapy.Spider):
    name = "lacapital"

    def start_requests(self):
        
        urls = [
            'https://www.lacapital.com.ar/secciones/politica.html',
            'https://www.lacapital.com.ar/secciones/economia.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1]
        noticias = set(response.xpath('//div[@class="summary-news-list"]/article/header/h1/a/@href').extract())
        for noticia in noticias:
            yield scrapy.Request(url=noticia, callback=self.parse_noticia)


    def parse_noticia(self, response):
        fecha_texto =  response.xpath('//p[@class="news-body-paragraph paragraph-date"]/text()').extract()[0]
        try:
            noticia_fecha = datetime.datetime.strptime(fecha_texto.split('-')[1].strip(), '%A  %d de %B de %Y')
        except:
            noticia_fecha = datetime.datetime.now()
        
        try:
            noticia_teaser = response.xpath('//div[@class="news-header-description"]/text()').extract()[0].strip()
        except:
            noticia_teaser = ''
            
        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@id="note-body"]/p/text()').extract()])

        data = {
            'titulo': response.xpath('//h1[@class="news-header-title"]/text()').extract()[0],
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'La Capital',
            'formato': 'web'
        }

        yield data
        
    
