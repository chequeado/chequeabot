import datetime

import scrapy
import newspaper

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_AR.utf8")

BASE_URL = 'https://www.lmneuquen.com/'

class LMNeuquenSpider(scrapy.Spider):
    name = "lmneuquen"

    def start_requests(self):
        
        urls = [
            'https://www.lmneuquen.com/contenidos/neuquen.html',
            'https://www.lmneuquen.com/contenidos/pais.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)


    def parse_seccion(self, response):
        seccion = response.url.split('/')[-1]
        noticias = set(response.xpath('//div[@class="col-66"]//h3[@itemprop="headline"]/a/@href').extract())

        for noticia in noticias:
            nota = response.urljoin(noticia)
            yield scrapy.Request(url=nota, callback=self.parse_noticia)


    def parse_noticia(self, response):
        
        noticia_titulo = response.xpath('//h1[@itemprop="headline"]/text()').extract()[0]
        try:
            fecha_texto = response.xpath('//span[@itemprop="datePublished"]/text()').extract()[0]
            noticia_fecha = datetime.datetime.strptime(fecha_texto, '%d %B %Y')
        except:
            noticia_fecha = datetime.datetime.now()
        
        try:
            noticia_teaser = response.xpath('//p[@itemprop="about"]/text()').extract()[0].strip()
        except:
            noticia_teaser = ''
        noticia_cuerpo = ' '.join([e for e in response.xpath('//div[@itemprop="articleBody"]/p/text()').extract()])

        data = {
            'titulo': noticia_titulo,
            'fecha': noticia_fecha,
            'noticia_texto': noticia_teaser + ' ' + noticia_cuerpo,
            'noticia_url': response.url,
            'source': 'LMNeuquen',
            'formato': 'web'
        }

        yield data
        
    
