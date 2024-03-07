from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.loader.processors import MapCompose
import random
import time


def cambiar_paginacion(enlace_inicial):
    # Verificamos si el enlace inicial tiene un parámetro de inicio de paginación
    if '&inicio=' in enlace_inicial:
        # Extraemos el número de página actual del enlace inicial
        inicio_actual = int(enlace_inicial.split('&inicio=')[1])
        # Calculamos el número de página siguiente
        siguiente_pagina = inicio_actual + 20
        # Reemplazamos el número de página en el enlace
        return enlace_inicial.split('&inicio=')[0] + f"&inicio={siguiente_pagina}"
    else:
        # Si no tiene un parámetro de inicio de paginación, asumimos que estamos en la primera página
        return enlace_inicial + "&inicio=21"


user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]


class Articulo(Item):
    Titulo = Field()
    Autor = Field()
    Revista = Field()
    Resumen = Field()
    Link = Field()


class Dialnet_spider(Spider):
    name = 'dialnet'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 24,
        'DOWNLOAD_DELAY': 10,
        'USER_AGENT': random.choice(user_agent_list),
        'FEED_URI': 'articulos_dialnet.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf8',
        # Agregar el código de estado 503 a los códigos de reintentos
        'RETRY_HTTP_CODES': [503],
        # Número de veces que se reintenta antes de considerar que ha fallado definitivamente
        'RETRY_TIMES': 3,
        'RETRY_DELAY': 5,  # Tiempo de espera en segundos entre cada reintento
    }

    start_urls = [
        'https://dialnet.unirioja.es/buscar/documentos?querysDismax.DOCUMENTAL_TODO=%22ciencias+sociales+computacionales%22+AND+%28%22estudios+sociales%22+OR+%22fenomenos+sociales%22+OR+impacto+OR+PLN+OR+NLP+OR+Bigdata+OR+IA+OR+%22Web+scraping%22+OR+Embbeding%29'
    ]

    def parse(self, response):
        sel = Selector(response)
        articulos = sel.xpath('//ul[@id="listadoDeArticulos"]/li')
        time.sleep(random.uniform(1, 2))

        for articulo in articulos:
            link_articulo = articulo.xpath(
                './/span[@class="titulo"]/a/@href').get()
            link_completo = response.urljoin(link_articulo)
            yield Request(link_completo, callback=self.parse_article)
            time.sleep(random.uniform(1, 3))

        siguiente = sel.xpath(
            '//div[@id="pieDeListadoDeBusquedaDeAutores"]/ul[@class="multipagina"]//a[@class="boton"]/@href').get()

        next_link = cambiar_paginacion(response.url)

        if siguiente:
            yield Request(next_link, callback=self.parse)
        else:
            print('***' * 30)
            print('Fin del escrapeo')
            print('***' * 30)

    def parse_article(self, response):

        item = ItemLoader(Articulo(), response)
        item.add_xpath('Titulo', '//div[@id="principal"]//h2/span/text()')
        autor = response.xpath(
            '//ul[@id="informacion"]/li[1]//span/a/text()').get()
        if autor:
            item.add_value('Autor', autor)
        else:
            item.add_value('Autor', 'Null')
        revista = response.xpath(
            '//div[@id="principal"]//ul[@id="informacion"]/li[2]/span/a/text()').get()
        if revista:
            item.add_value('Revista', revista)
        else:
            item.add_value('Revista', 'Null')
        resumen = response.xpath('//ul[@id="resumen"]/li//p/text()').getall()
        if resumen:
            item.add_value('Resumen', resumen)
        else:
            item.add_value('Resumen', 'Null')
        link_articulo = response.xpath('//li[@id="enlaces"]//a/@href').get()
        if link_articulo:
            link_articulo_completo = response.urljoin(link_articulo)
            item.add_value('Link', link_articulo_completo)
        else:
            item.add_value('Link', 'Null')
        yield item.load_item()
        time.sleep(random.uniform(1, 3))
