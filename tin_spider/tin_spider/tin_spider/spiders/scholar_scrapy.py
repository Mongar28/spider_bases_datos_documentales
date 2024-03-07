# VER RECURSOS DE LA CLASE PARA INSTALAR SCRAPY
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from scrapy.http import Request
import random
import time
import re

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def generar_enlace_siguiente_pagina(url_inicial):
    # Analiza la URL y los parámetros de consulta
    url_parsed = urlparse(url_inicial)
    params = parse_qs(url_parsed.query)

    # Incrementa el valor 'from' y 'page'
    params['from'] = [str(int(params['from'][0]) + 15)]
    params['page'] = [str(int(params['page'][0]) + 1)]

    # Construye la URL de la siguiente página
    url_next = urlunparse(
        (
            url_parsed.scheme,
            url_parsed.netloc,
            url_parsed.path,
            url_parsed.params,
            urlencode(params, doseq=True),
            url_parsed.fragment,
        )
    )

    return url_next

# Lista de agentes de usuario


user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]

# ABSTRACCION DE DATOS A EXTRAER - DETERMINA LOS DATOS QUE TENGO QUE LLENAR Y QUE ESTARAN EN EL ARCHIVO GENERADO


class Articulo(Item):

    Titulo = Field()
    Fecha = Field()
    Autor = Field()
    Descargas = Field()
    Resumen = Field()
    Link = Field()

# CLASE CORE - SPIDER


class Scielo_spider(Spider):
    name = 'scholar'  # nombre, puede ser cualquiera

    # Forma de configurar el USER AGENT en scrapy
    # Configuración personalizada del proceso de crawling
    custom_settings = {
        'CONCURRENT_REQUESTS': 24,  # Número máximo de solicitudes simultáneas
        'MEMUSAGE_LIMIT_MB': 2048,  # Límite máximo de uso de memoria
        'USER_AGENT': user_agent_list[random.randint(0, len(user_agent_list) - 1)],
        'ROBOTSTXT_OBEY': False,  # Respetar las reglas del archivo robots.txt
        # Codificación de salida para los datos recolectados
        'FEED_EXPORT_ENCODING': 'utf8',
        'FEED_URI': 'articulos_scielo_2.json',  # Ruta de salida del archivo JSON
        'FEED_FORMAT': 'json',  # Formato de salida del archivo JSON
        'DOWNLOAD_DELAY': 2,
        'DOWNLOAD_DELAY_FACTOR': 0.5,
        'DOWNLOAD_DELAY_RANDOMIZE': True  # Retraso entre solicitudes consecutivas
    }

    # URL SEMILLA
    start_urls = [
        'https://scholar.google.com/scholar?as_vis=1&q=ciencias+sociales+computacionales&hl=es&as_sdt=0,5'
    ]

    # Funcion que se va a llamar cuando se haga el requerimiento a la URL semilla

    def parse(self, response):
    
        # Selectores: Clase de scrapy para extraer datos
        sel = Selector(response)
      
        articulos = sel.xpath(
            '//div[@class="gs_r gs_or gs_scl"]')
        print('*' * 100)
        print(len(articulos))
        print('*' * 100)
        
        for articulo in articulos:
            art = articulo.xpath('.//h3[@class="gs_rt"]/a//text()').getall()
            print('*' * 100)
            print(art)
            print('*' * 100)
