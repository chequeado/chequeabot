import datetime

import newspaper
import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.elindependiente.com.ar/'

class ElIndependienteSpider(scrapy.Spider):
    name = "elindependiente"

    def start_requests(self):
        
        urls = [
            'http://www.elindependiente.com.ar/seccion.php?seccion=1',
            'http://www.elindependiente.com.ar/seccion.php?seccion=5'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1]

        noticias = set(response.xpath('//a/@href').extract())
        noticias = [BASE_URL + p for p in noticias if 'pagina.php' in p]
        
        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)



    def parse_noticia(self, response):
        fecha_texto = response.xpath('//p[@class="right"]/text()').extract()[0]
        noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d/%m/%y')
        noticia_fecha = datetime.datetime.now()
        noticia_teaser = response.xpath('//p[@class="text-justify"]/text()').extract()[0]
        noticia_titulo = response.xpath('//h4[@class="font-weight-bold"]/text()').extract()[0]    
        noticia_cuerpo = ' '.join([e for e in response.xpath('//p[@style="text-align: justify;"]/text()').extract()])

        data = {
            'titulo': noticia_titulo,
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'El Independiente',
            'formato': 'web'
        }

        yield data
