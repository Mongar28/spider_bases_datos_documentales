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

    # Obtenemos el valor de 'start' o establecemos en 0 si no está presente
    start_value = int(params.get('start', ['0'])[0])

    # Incrementamos el valor de 'start' en 10 para obtener la siguiente página
    params['start'] = [str(start_value + 10)]

    # Construimos la URL de la siguiente página
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
    Citas = Field()
    #Resumen = Field()
    Link = Field()

# CLASE CORE - SPIDER


class Scielo_spider(Spider):
    name = 'scholar'  # nombre, puede ser cualquiera

    # Forma de configurar el USER AGENT en scrapy
    # Configuración personalizada del proceso de crawling
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 24,
        'DOWNLOAD_DELAY': 10,
        'USER_AGENT': random.choice(user_agent_list),
        'FEED_URI': 'articulos_scholar.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf8',
        # Agregar el código de estado 503 a los códigos de reintentos
        'RETRY_HTTP_CODES': [503],
        # Número de veces que se reintenta antes de considerar que ha fallado definitivamente
        'RETRY_TIMES': 3,
        'RETRY_DELAY': 5,  # Tiempo de espera en segundos entre cada reintento
    }

    # URL SEMILLA
    start_urls = [
        'https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&as_vis=1&q=%22ciencias+sociales+computacionales%22+AND+%28%22estudios+sociales%22+OR+%22fenomenos+sociales%22+OR+impacto+OR+PLN+OR+NLP+OR+Bigdata+OR+IA+OR+%22Web+scraping%22+OR+Embbeding%29&btnG='
    ]

    # Funcion que se va a llamar cuando se haga el requerimiento a la URL semilla

    def parse(self, response):
    
        # Selectores: Clase de scrapy para extraer datos
        sel = Selector(response)
      
        articulos = sel.xpath(
            '//div[@class="gs_r gs_or gs_scl"]')
        
        for articulo in articulos:
            
            # titulo
            titulo = articulo.xpath('.//h3[@class="gs_rt"]/a//text()').getall()
            titulo = "".join(titulo).strip().replace('  ', ' ')
            
            # Autor
            autor = articulo.xpath('.//div[@class="gs_ri"]/div[@class="gs_a"]//text()').getall()
            autor = ",".join(autor)
            
            autor = autor.split('-')
            print("*" * 100)
            print(autor[0])
            print("*" * 100)
            
            
            # Fecha   
            info_articulo = articulo.xpath('.//div[@class="gs_ri"]/div[@class="gs_a"]//text()').getall()

            patron_fecha = r'\d{4}'
            search_fecha = re.search(patron_fecha, info_articulo[-1])
            
            if search_fecha:
                fecha = search_fecha.group()
            else:
                fecha = 'Null'
            
                        
            # Citas
            citas = articulo.xpath('.//div[@class="gs_ri"]/div[@class="gs_fl gs_flb"]/a[3]/text()').get()
            
            if re.search(r'Citado', citas):
                num_citas = re.search(r'\d{1,9}', citas).group()
            else:
                num_citas = '0'
            
            item = ItemLoader(Articulo(), articulo)
            
            item.add_value('Titulo', titulo)
            item.add_value('Fecha', fecha)
            item.add_value('Autor', autor)
            item.add_value('Citas', num_citas)
            item.add_xpath('Link', './/div[@class="gs_or_ggsm"]/a/@href')
   
            yield item.load_item()
            time.sleep(random.uniform(1, 2))
        
        # obtener el enlace a la siguiente página
        siguiente = sel.xpath(
            '//div[@id="gs_nm"]/button[@type="button"][2]/span[@class="gs_wr"]/span[@class="gs_ico"]').get()
        
        url_next = response.url
        # url_next= re.sub(r'page=(\d+)', 'page={}'.format(numero), url_next)

       # Genera la URL de la siguiente página
        url_siguiente = generar_enlace_siguiente_pagina(url_next)
        print(url_siguiente)

        if siguiente is not None:
            yield response.follow(url_siguiente, self.parse)
            
