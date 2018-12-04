import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'https://www.casarosada.gob.ar/'

class CasaRosadaSpider(scrapy.Spider):
    name = "casarosada"

    def start_requests(self):
        
        urls = [
            'https://www.casarosada.gob.ar/informacion/conferencias?limitstart=0',
            'https://www.casarosada.gob.ar/informacion/discursos?limitstart=0'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        noticias = set(response.xpath('//div[@class="item"]//a/@href').extract())

        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):
        
        noticia_titulo = response.xpath('//div[@class="panel panel-default col-md-8 col-md-offset-2 jumbotron-hero"]/h2/strong/text()').extract()[0].strip()
        try:
            fecha_texto = response.xpath('//time[@class="pull-right"]/text()').extract()[0].strip()
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%A %d de %B de %Y')
        except:
            noticia_fecha = datetime.datetime.now()
        
        noticia_teaser = ''
        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@class="col-md-8 col-md-offset-2"]/p/text()').extract()])

        data = {
            'titulo': noticia_titulo,
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'Casa Rosada',
            'formato': 'web'
        }

        yield data
        
    
