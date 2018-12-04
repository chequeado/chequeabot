import datetime

from newspaper import Article

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'https://www.pagina12.com.ar/'

class PaginaSpider(scrapy.Spider):
    name = "p12"

    def start_requests(self):
        
        url = 'https://www.pagina12.com.ar/edicion-impresa/'
        secciones = ['el-pais']
        for seccion in secciones:
            #https://www.pagina12.com.ar/edicion-impresa/19-07-2017
            yield scrapy.Request(url=url, meta={'seccion': seccion},  callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.meta['seccion']
        anchor = response.xpath('//span[@id="%s"]' % seccion)[0]
        ul = anchor.xpath('following-sibling::*[2]')[0]
        noticias = ul.xpath('li/div/div/div[@class="article-box__container"]/h2/a')
        for noticia in noticias:
            nn = noticia.xpath('@href')[0]
            noticia_url = nn.extract()
            yield scrapy.Request(url=noticia_url, callback=self.parse_noticia)


    def parse_noticia(self, response):
        ff = Article(response.url)
        ff.download()
        ff.parse()
        texto = ff.text
        titulo = ff.title
        noticia_url = ff.url
        noticia_fecha = ff.publish_date
        
        data = {
            'titulo': titulo,
            'fecha': noticia_fecha,
            'noticia_texto': texto,
            'noticia_url': noticia_url,
            'source': 'pagina12',
            'formato': 'web'
        }
        yield data
        
    
