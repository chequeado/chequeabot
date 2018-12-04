#!/usr/    bin/python
# -*- coding: utf-8 -*-

import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.eldia.com/'

class ElDiaSpider(scrapy.Spider):
    name = "eldia"

    def start_requests(self):
        
        urls = [
            'http://www.eldia.com/seccion/politica-y-economia'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        noticias = set(response.xpath('//div[@id="main_seccion"]/article//a/@href').extract())

        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):
        
        try:
            fecha_texto =  response.xpath('//span[@itemprop="datePublished"]/span[@class="article-date today"]/text()').extract()[0].split('|')[0].strip()
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d de %B de %Y')
        except:
            noticia_fecha = datetime.datetime.now()
        
        try:
            noticia_teaser = response.xpath('//p[@class="bajada"]/text()').extract()[0].strip()
        except:
            noticia_teaser = ''

        noticia_cuerpo = ' '.join([e for e in  response.xpath('//div[@itemprop="articleBody"]/p/text()').extract()])

        data = {
            'titulo': response.xpath('//h2[@itemprop="headline"]/text()').extract()[0],
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'El Día',
            'formato': 'web'
        }

        yield data
        
    
