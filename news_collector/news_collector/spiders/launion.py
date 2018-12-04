import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'https://www.launiondigital.com.ar/'

class LaUnionSpider(scrapy.Spider):
    name = "launion"

    def start_requests(self):
        
        urls = [
            'https://www.launiondigital.com.ar/secciones/politica',
            'https://www.launiondigital.com.ar/secciones/economia-y-finanzas'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1]
        noticias = set(response.xpath('//div[@class="content-node"]//a[contains(@href, "/noticias/")]/@href').extract())

        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):
        try:
            fecha_texto =  response.xpath('//div[@class="lu-author-info"]/time/text()').extract()[0].split('-')[0].strip()
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%A, %d %B, %Y')
        except:
            noticia_fecha = datetime.datetime.now()
        
        try:
            noticia_teaser = response.xpath('//div[@class="copete"]/text()').extract()[0]
        except:
            noticia_teaser = ''

        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@class="cuerpo-noticia"]//p/text()').extract()])

        data = {
            'titulo': response.xpath('//h1[@id="page-title"]/text()').extract()[0],
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'La Union Digital',
            'formato': 'web'
        }

        yield data
        
    
