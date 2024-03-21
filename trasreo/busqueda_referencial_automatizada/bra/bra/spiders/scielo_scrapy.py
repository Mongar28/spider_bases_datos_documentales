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
    params["from"] = [str(int(params["from"][0]) + 15)]
    params["page"] = [str(int(params["page"][0]) + 1)]

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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
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
    name = "scielo"  # nombre, puede ser cualquiera

    # Forma de configurar el USER AGENT en scrapy
    # Configuración personalizada del proceso de crawling
    custom_settings = {
        "CONCURRENT_REQUESTS": 24,  # Número máximo de solicitudes simultáneas
        "MEMUSAGE_LIMIT_MB": 2048,  # Límite máximo de uso de memoria
        "USER_AGENT": user_agent_list[random.randint(0, len(user_agent_list) - 1)],
        "ROBOTSTXT_OBEY": False,  # Respetar las reglas del archivo robots.txt
        # Codificación de salida para los datos recolectados
        "FEED_EXPORT_ENCODING": "utf8",
        "FEED_URI": "archivos/articulos_scielo.csv",  # Ruta de salida del archivo JSON
        "FEED_FORMAT": "csv",  # Formato de salida del archivo JSON
        "DOWNLOAD_DELAY": 2,
        "DOWNLOAD_DELAY_FACTOR": 0.5,
        "DOWNLOAD_DELAY_RANDOMIZE": True,  # Retraso entre solicitudes consecutivas
    }

    # URL SEMILLA
    start_urls = [
        "https://search.scielo.org/?q=(((Pacifismo+or+Noviolencia+or+paz+or+paz+positiva+or+Coexistencia+pac%C3%ADfica+or+soluci%C3%B3n+de+conflictos+or+mediaci%C3%B3n+or+Consolidaci%C3%B3n+de+la+paz+or+Mantenimiento+de+la+paz+or+Restablecimiento+de+la+paz)+and+(Territorio+or+movimiento+social+or+sociedad+or+comunidad+or+grupo)))+OR+(((Modelo+educativo+or+modelo+educacional+or+investigaci%C3%B3n+pedag%C3%B3gica+or+sistema+educativo+or+pr%C3%A1ctica+pedag%C3%B3gica+or+experiencia+pedag%C3%B3gica)+and+(educaci%C3%B3n+para+la+paz+or+Cultura+de+paz++or+educaci%C3%B3n+ciudadana+or+educaci%C3%B3n+moral+or+educaci%C3%B3n+para+los+derechos+humanos)))&lang=es&count=15&from=1&output=site&sort=&format=summary&fb=&page=1&filter%5Bsubject_area%5D%5B%5D=Human+Sciences&filter%5Bsubject_area%5D%5B%5D=Applied+Social+Sciences&filter%5Bwok_subject_categories%5D%5B%5D=social&filter%5Bwok_subject_categories%5D%5B%5D=multidisciplinary&filter%5Bwok_subject_categories%5D%5B%5D=educational&filter%5Bwok_subject_categories%5D%5B%5D=education&filter%5Bwok_subject_categories%5D%5B%5D=sociology&filter%5Bwok_subject_categories%5D%5B%5D=relations&filter%5Bwok_subject_categories%5D%5B%5D=communication&q=((%22Pacifismo%22+OR+%22Noviolencia%22+OR+%22paz%22+OR+%22paz+positiva%22+OR+%22Coexistencia+pac%C3%ADfica%22+OR+%22soluci%C3%B3n+de+conflictos%22+OR+%22mediaci%C3%B3n%22+OR+%22Consolidaci%C3%B3n+de+la+paz%22+OR+%22Mantenimiento+de+la+paz%22+OR+%22Restablecimiento+de+la+paz%22)+AND+(%22Territorio%22+OR+%22movimiento+social%22+OR+%22sociedad%22+OR+%22comunidad%22+OR+%22grupo%22))+OR+(((%22Modelo+educativo%22+OR+%22modelo+educacional%22+OR+%22investigaci%C3%B3n+pedag%C3%B3gica%22+OR+%22sistema+educativo%22+OR+%22pr%C3%A1ctica+pedag%C3%B3gica%22+OR+%22experiencia+pedag%C3%B3gica%22)+AND+(%22educaci%C3%B3n+para+la+paz%22+OR+%22Cultura+de+paz%22+OR+%22educaci%C3%B3n+ciudadana%22+OR+%22educaci%C3%B3n+moral%22+OR+%22educaci%C3%B3n+para+los+derechos+humanos%22)))&lang=es&page=1"
    ]

    # Funcion que se va a llamar cuando se haga el requerimiento a la URL semilla

    def parse(self, response):
        # Selectores: Clase de scrapy para extraer datos
        sel = Selector(response)
        articulos = sel.xpath(
            '//div[@class = "results"]//div[@class = "col-md-11 col-sm-10 col-xs-11"]'
        )

        for articulo in articulos:
            item = ItemLoader(Articulo(), articulo)
            item.add_xpath(
                "Titulo", './/div[@class = "line"]/a/strong[@class = "title"]/text()'
            )
            item.add_xpath("Fecha", './/div[@class= "line source"]/span[3]/text()')
            item.add_xpath(
                "Autor", './/div[@class = "line authors"]/a[@class = "author"]//text()'
            )
            descargas = "".join(
                articulo.xpath('.//div[@class = "line metadata"]//strong/text()').re(
                    r"\d+"
                )
            )
            descargas = str(descargas) if descargas else "0"
            item.add_value("Descargas", descargas)

            print("*" * 100)
            print(descargas, type(descargas))
            print("*" * 100)

            resumen = (
                "".join(
                    articulo.xpath(
                        './/div[@class = "user-actions"]/div[contains(@id, "_es")]/text()'
                    ).extract()
                )
                .replace("\n", " ")
                .strip()
            )
            item.add_value("Resumen", resumen)
            item.add_xpath("Link", './/div[@class = "line"]/a/@href')

            yield item.load_item()
            time.sleep(random.uniform(1, 2))

        # obtener el enlace a la siguiente página
        siguiente = sel.xpath(
            '//div[@class = "col-md-6 right"]/a[@class = "pageNext"]'
        ).get()
        numero = sel.xpath('//div[@class = "col-md-6 right"]/input/@value')
        url_next = response.url
        # url_next= re.sub(r'page=(\d+)', 'page={}'.format(numero), url_next)

        # Genera la URL de la siguiente página
        url_siguiente = generar_enlace_siguiente_pagina(url_next)

        if siguiente is not None:
            yield response.follow(url_siguiente, self.parse)
