import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.diariolavozdelchaco.com/'

class LaVozDelChacoSpider(scrapy.Spider):
    name = "lavozdelchaco"

    def start_requests(self):
        
        urls = [
            'http://www.diariolavozdelchaco.com/notix/noticias/1/politica-nacional.htm',
            'http://www.diariolavozdelchaco.com/notix/noticias/1/politica-provincial.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1]
        noticias = set(response.xpath('//div[@class="portfolio-desc"]//a/@href').extract())

        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):   
        try:
            fecha_texto = response.xpath('//ul[@class="entry-meta clearfix"]//li/text()').extract()[4]
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d de %B de %Y') 
        except:
            noticia_fecha = datetime.datetime.now()

        noticia_cuerpo = ' '.join([e.strip().replace('“','"').replace('″','"').replace('”','"') for e in response.xpath('//div[@class="entry-content notopmargin"]//text()').extract()])
        noticia_titulo = response.url.split("_")[1].split(".")[0].replace("-"," ").capitalize()    
    
        data = {
            'titulo': noticia_titulo,
            'fecha': noticia_fecha,
            'noticia_texto': noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'La Voz del Chaco',
            'formato': 'web'
        }
        
        yield data
        
    
