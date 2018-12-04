import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.lavoz.com.ar'

class LaVozSpider(scrapy.Spider):
    name = "lavoz"

    def start_requests(self):
        
        urls = [
            'http://www.lavoz.com.ar/search/lavoz/politica',
            'http://www.lavoz.com.ar/search/lavoz/negocios'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1]
        noticias = response.xpath('//div[@class="nodos-list clearfix"]/article/div/main/div[@class="contenido"]/header/h2/a[contains(@href, "/%s")]' % seccion)

        for noticia in noticias:
            nn = noticia.xpath('@href')[0]
            noticia_url = BASE_URL + nn.extract()
            yield scrapy.Request(url=noticia_url, callback=self.parse_noticia)


    def parse_noticia(self, response):
        fecha_texto =  response.xpath('//time/text()')[0].extract().strip().split(',')[0]
        #FIXME: detecting url redirect: http://www.lavoz.com.ar/negocios/maquinaria-vial-la-estrella-de-la-jornada-entre-pauny-y-la-voz -> http://www.agrovoz.com.ar/actualidad/maquinaria-vial-la-estrella-de-la-jornada-entre-pauny-y-la-voz

        noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d de %B de %Y')
        noticia_teaser = ' '.join([e for e in response.xpath('//div/main/div[@class="teaser"]/p//text()').extract()])
        noticia_cuerpo = ' '.join([e for e in response.xpath('//div/main/loginwall/div[@class="body"]/p//text()').extract()])

        data = {
            'titulo': response.xpath('//div[@class="contenido-titulo"]/h1/text()').extract()[0],
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'la voz del interior',
            'formato': 'web'
        }
        yield data
        
    
