import datetime

import newspaper
import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.laarena.com.ar/'

class LaArenaSpider(scrapy.Spider):
    name = "laarena"

    def start_requests(self):
        
        urls = [
            'http://www.laarena.com.ar/category/el_pais',
            'http://www.laarena.com.ar/category/la_pampa'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1] #ejemplo: la_pampa
        noticias = response.xpath('//a[contains(@href,"' + seccion +'-")]/@href').extract()
        
        #la arena tiene urls de este estilo:
        # http://www.laarena.com.ar/la_pampa-se-posterga-el-1-encuentro-de-artesanias-por-mal-tiempo-2018676-163.htm
        #la seccion la_pampa esta por delante de la url especifica del articulo, por lo tanto
        #hay que utilizar ese indicador para determinar la seccion de cada articulo

        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)
        

    def parse_noticia(self, response):
        ff = newspaper.Article(response.url)
        ff.download()
        ff.parse()
        texto = ff.text.replace('“','"').replace('″','"').replace('”','"')
        titulo = ff.title
        noticia_url = ff.url
        noticia_fecha = ff.publish_date if ff.publish_date else datetime.datetime.now()

        data = {
            'titulo': titulo,
            'fecha': noticia_fecha,
            'noticia_texto': texto,
            'noticia_url': noticia_url,
            'source': 'La Arena',
            'formato': 'web'
        }

        yield data
        
    
