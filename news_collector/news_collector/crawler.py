# -*- coding: utf-8 -*-

import datetime

# import the spiders you want to run
from spiders.clarin import ClarinSpider
from spiders.infobae import InfobaeSpider
from spiders.lavoz import LaVozSpider
from spiders.minutouno import MinutoUnoSpider
from spiders.pagina12 import PaginaSpider
from spiders.pagina12_economia import PaginaEcoSpider
from spiders.losandes import LosAndesSpider
from spiders.diarioprensa import DiarioPrensaSpider
from spiders.diariorionegro import DiarioRioNegroSpider
from spiders.elchubut import ElChubutSpider
from spiders.elindependiente import ElIndependienteSpider
from spiders.ellitoral import ElLitoralSpider
from spiders.elterritorio import ElTerritorioSpider
from spiders.laarena import LaArenaSpider
from spiders.lacapital import LaCapitalSpider
from spiders.lagaceta import LaGacetaSpider
from spiders.lagacetasalta import LaGacetaSaltaSpider
from spiders.larepublica import LaRepublicaSpider
from spiders.launion import LaUnionSpider
from spiders.lavozdelchaco import LaVozDelChacoSpider
from spiders.lmneuquen import LMNeuquenSpider
from spiders.rosadadiscursos import CasaRosadaSpider
from spiders.lamaniana import LaManianaSpider
from spiders.eldia import ElDiaSpider
from spiders.lacapitalmdp import LaCapitalMdpSpider
from spiders.diariodelfindelmundo import DiarioDelFinDelMundoSpider

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from credentials import *


settings = get_project_settings()
settings = Settings()

settings.set("ITEM_PIPELINES", {"pipelines.MySQLPipeline": 300})

# list of crawlers
TO_CRAWL = [ClarinSpider, InfobaeSpider, LaVozSpider, MinutoUnoSpider, PaginaSpider,
            PaginaEcoSpider, LosAndesSpider, DiarioRioNegroSpider,
            ElChubutSpider, ElIndependienteSpider, ElLitoralSpider,
            ElTerritorioSpider, LaArenaSpider, LaCapitalSpider,
            LaGacetaSpider, LaGacetaSaltaSpider, LaRepublicaSpider, LaUnionSpider,
            LaVozDelChacoSpider, LMNeuquenSpider, CasaRosadaSpider,
            LaManianaSpider, ElDiaSpider, LaCapitalMdpSpider, DiarioDelFinDelMundoSpider,
            DiarioPrensaSpider]

configure_logging()
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    for spider in TO_CRAWL:
        yield runner.crawl(spider)
    reactor.stop()


crawl()
reactor.run() # the script will block here until the last crawl call is finished
