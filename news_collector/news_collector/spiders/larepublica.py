import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.eldiariodelarepublica.com/'

class LaRepublicaSpider(scrapy.Spider):
    name = "larepublica"

    def start_requests(self):
        
        urls = [
            'http://www.eldiariodelarepublica.com/seccion/pais',
            'http://www.eldiariodelarepublica.com/seccion/provincia'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1]
        noticias = set(response.xpath('//div[@id="cont_seccion"]//a[contains(@href, "/nota/")]/@href').extract())

        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):
        
        try:
            fecha_texto =  response.xpath('//p[@class="news-body-paragraph paragraph-date"]/text()').extract()[0]
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%A %d de %B de %Y')
        except:
            noticia_fecha = datetime.datetime.now()
            
        noticia_teaser = response.xpath('//div[@class="np_nota_descripcion"]/p/text()').extract()[0]
        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@id="notapage_texto"]/p/text()').extract()])

        data = {
            'titulo': response.xpath('//h2[@id="title"]/text()').extract()[0],
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'La Republica',
            'formato': 'web'
        }

        yield data
        
    
