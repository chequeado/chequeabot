# -*- coding: utf-8 -*-

import scrapy


class NewsItem(scrapy.Item):
    titulo = scrapy.Field()
    noticia_texto = scrapy.Field()
    source = scrapy.Field()
    noticia_url = scrapy.Field()
    fecha = scrapy.Field()
    formato = scrapy.Field()
