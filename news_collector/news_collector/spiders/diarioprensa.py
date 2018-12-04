import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.diarioprensa.com.ar/'

class DiarioPrensaSpider(scrapy.Spider):
    name = "diarioprensa"

    def start_requests(self):
        
        urls = [
            'http://www.diarioprensa.com.ar/category/politica/',
            'http://www.diarioprensa.com.ar/category/economia/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        noticias = set(response.xpath('//main[@id="main"]/article/header/h2/a/@href').extract())

        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):

        noticia_titulo = response.xpath('//h1[@class="entry-title"]/text()').extract()[0]
        try:
            fecha_texto = response.xpath('//time/text()').extract()[0].strip()
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d %B, %Y')
        except:
            noticia_fecha = datetime.datetime.now()

        noticia_teaser = ''
        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@class="entry-content"]/p/text()').extract()])

        data = {
            'titulo': noticia_titulo,
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'Diario Prensa',
            'formato': 'web'
        }

        yield data
        
    