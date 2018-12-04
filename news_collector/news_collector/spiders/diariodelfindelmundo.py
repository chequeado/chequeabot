import datetime

import scrapy

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'http://www.eldiariodelfindelmundo.com/'

class DiarioDelFinDelMundoSpider(scrapy.Spider):
    name = "diariodelfindelmundo"

    def start_requests(self):
        
        urls = [
            'http://www.eldiariodelfindelmundo.com/provinciales/',
            'http://www.eldiariodelfindelmundo.com/municipales/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        noticias = set(response.xpath('//div[@class="contenedor_general_resultados"]//h4[@class="titulo_listado_resultados "]/a/@href').extract())
        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):
        noticia_titulo = response.xpath('//h3[@class="titulo_individual_noticia"]/text()')[0].extract().strip()
        try:
            fecha_texto = response.xpath('//div[@class="fecha_individual_noticia"]/text()').extract()[0].strip()
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d/%m/%Y')
        except:
            noticia_fecha = datetime.datetime.now()

        noticia_teaser = ''
        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@class="contenido_individual_noticia"]/p/text()').extract()])

        data = {
            'titulo': noticia_titulo,
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'Diario del Fin del Mundo',
            'formato': 'web'
        }

        yield data
        
    
