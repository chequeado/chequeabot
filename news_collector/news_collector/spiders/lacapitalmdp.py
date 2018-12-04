#!/usr/    bin/python
# -*- coding: utf-8 -*-

import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.lacapitalmdp.com/'

class LaCapitalMdpSpider(scrapy.Spider):
    name = "lacapitalmdp"

    def start_requests(self):
        
        urls = [
            'http://www.lacapitalmdp.com/categorias/el-pais/',
            'http://www.lacapitalmdp.com/categorias/la-ciudad/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        noticias = set(response.xpath('//div[@class="col-xs-12 col-sm-9 col-md-7 col-lg-7 posts_list"]/div[@class="category_nota"]/h2/a/@href').extract())
        
        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):
        
        try:
            fecha_texto = response.xpath('//div[@class="date_container"]/text()').extract()[0].strip()
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d de %B de %Y')
        except:
            noticia_fecha = datetime.datetime.now()
        
        try:
            noticia_teaser = response.xpath('//div[@class="bajada"]/p/text()').extract()[0].strip()
        except:
            noticia_teaser = ''

        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@class="nota_content"]/p//text()').extract()])

        data = {
            'titulo': response.xpath('//div[@class="col-xs-12 col-sm-9 col-md-6 col-lg-7"]/h1/text()').extract()[0].strip(),
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'La Capital Mar del Plata',
            'formato': 'web'
        }
        
        yield data
        
    
