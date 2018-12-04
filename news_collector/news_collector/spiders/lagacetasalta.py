import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'https://www.lagacetasalta.com.ar/'

class LaGacetaSaltaSpider(scrapy.Spider):
    name = "lagacetasalta"

    def start_requests(self):
        
        urls = [
            'https://www.lagacetasalta.com.ar/politica',
            'https://www.lagacetasalta.com.ar/economia'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1]
        noticias = set(response.xpath('//a[contains(@href, "/nota/")]/@href').extract())

        for noticia in noticias:
            nota = noticia
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):

        try:
            fecha_texto =  response.xpath('//p[@class="news-body-paragraph paragraph-date"]/text()').extract()[0]
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%A %d de %B de %Y')
        except:
            noticia_fecha = datetime.datetime.now()
        
        try:
            noticia_teaser = response.xpath('//h2[@itemprop="description"]/text()').extract()[0]
        except:
            noticia_teaser = ''

        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@class="newsBody"]/p/text()').extract()])

        data = {
            'titulo': response.xpath('//h1[@itemprop="headline"]/text()').extract()[0],
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'La Gaceta Salta',
            'formato': 'web'
        }

        yield data
        
    
