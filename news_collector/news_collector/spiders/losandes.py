import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.losandes.com.ar'

class LosAndesSpider(scrapy.Spider):
    name = "losandes"

    def start_requests(self):
        
        urls = [
            'http://www.losandes.com.ar/article/index?category=politica',
            'http://www.losandes.com.ar/article/index?category=economia'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1]
        noticias = response.xpath('//div[@class="row news-block"]//a[contains(@href, "/article/view?slug")]/@href').extract()

        for noticia in noticias:
            noticia_url = 'http:' + noticia
            yield scrapy.Request(url=noticia_url, callback=self.parse_noticia)


    def parse_noticia(self, response):
        fecha_texto =  response.xpath('//span[@class="separator"]/text()').extract()[0].strip()
        #FIXME: detecting url redirect: http://www.lavoz.com.ar/negocios/maquinaria-vial-la-estrella-de-la-jornada-entre-pauny-y-la-voz -> http://www.agrovoz.com.ar/actualidad/maquinaria-vial-la-estrella-de-la-jornada-entre-pauny-y-la-voz

        noticia_fecha = datetime.datetime.strptime(fecha_texto, '%A, %d de %B de %Y')
        noticia_teaser = response.xpath('//div[@class="resume-news"]/h3//text()').extract()[0].strip()
        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@class="main-col-article"]//p/text()').extract()])

        data = {
            'titulo': response.xpath('//div[@class="title-news"]/h1//text()').extract()[0].strip(),
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'Los Andes',
            'formato': 'web'
        }
        yield data
        
    
