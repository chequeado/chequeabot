import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://infobae.com'

class InfobaeSpider(scrapy.Spider):
    name = "infobae"

    def start_requests(self):
        
        urls = [
            'http://infobae.com/politica',
            'http://infobae.com/economia',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-2]
        noticias = response.xpath('//div[@class="result-listing"]/div/div[@class="generic-results-list-item pwa_card"]/article/header/div[@class="row"]/div[@class="col-sm-8"]/figure/a[contains(@href, "%s")]' % seccion)
        for noticia in noticias:
            nn = noticia.xpath('@href')[0]
            noticia_url = BASE_URL + nn.extract()
            yield scrapy.Request(url=noticia_url, callback=self.parse_noticia)


    def parse_noticia(self, response):
        fecha_texto =  response.xpath('//span[@class="byline-date"]/text()').extract()[0].strip()
        noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d de %B de %Y')
        data = {
            'titulo': response.xpath('//header[@class="article-header hed-first col-sm-12"]/h1/text()')[0].extract(),
            'fecha': noticia_fecha,
            'noticia_texto': ' '.join([e for e in response.xpath('//div[@id="article-content"]/div[@class="row"]/div/p//text()').extract()]),
            'noticia_url': response.url,
            'source': 'infobae',
            'formato': 'web'
        }
        yield data
        
    
