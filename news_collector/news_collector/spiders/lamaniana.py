#!/usr/    bin/python
# -*- coding: utf-8 -*-

import datetime
import locale

import scrapy

locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://xn--lamaanaonline-lkb.com.ar/'

class LaManianaSpider(scrapy.Spider):
    name = "lamaniana"

    def start_requests(self):
        
        urls = [
            'http://xn--lamaanaonline-lkb.com.ar/noticias/3-locales',
            'http://xn--lamaanaonline-lkb.com.ar/noticias/5-interior'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        noticias = set(response.xpath('//div[@class="columna-principal"]/div[@class="caja"]/div[@class="listar-txt"]/a/@href').extract())

        for noticia in noticias:
            nota = noticia
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):
        try:
            fecha_texto =  response.xpath('//div[@class="noticia-bajada"]/span[@class="label label-default"]/text()').extract()[0]
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d/%m/%Y')
        except:
            noticia_fecha = datetime.datetime.now()
        
        try:
            noticia_teaser = response.xpath('//div[@class="noticia-bajada"]/text()').extract()[0].strip()
        except:
            noticia_teaser = ''

        noticia_cuerpo = ' '.join([e for e in  response.xpath('//div[@class="noticia-texto"]//text()').extract()])

        data = {
            'titulo': response.xpath('//h1[@class="noticia-title"]/text()').extract()[0],
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'La Mañana',
            'formato': 'web'
        }

        yield data
        
    
