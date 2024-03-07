# Tutorial de Scrapy

### link: https://docs.scrapy.org/en/latest/intro/tutorial.html

## Inatalción 
```bash
pip install scrapy
```

## Creando un proyecto

Antes de empezar a escrapear, debes crear un proyecto en el directorio donde te gustaria trabajar. Solo tiene que ejecutar el siguiente comando.

```bash
scrapy startproject tutorial
```

```
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

## Nuestro primer Spider

Los Spiders son clases que defines y que Scrapy utiliza para extraer información de un sitio web (o un grupo de sitios web). Deben ser `subclases` de `Spider` y definir las solicitudes iniciales que se realizarán, opcionalmente cómo seguir enlaces en las páginas, y cómo analizar el contenido descargado de la página para extraer datos.

Este es el código para nuestro primer Spider. Guárdalo en un archivo llamado ` quotes_spider.py` en el directorio `tutorial/spiders` de tu proyecto:

```python
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
```
Como puedes ver, nuestro Spider es una subclase de scrapy.Spider y define algunos atributos y métodos:

- `name`: identifica al Spider. Debe ser único dentro de un proyecto, es decir, no puedes establecer el mismo nombre para diferentes Spiders.

- `start_requests()`: debe devolver un iterable de Requests (puedes devolver una lista de solicitudes o escribir una función generadora) desde el cual el Spider comenzará a rastrear. Las solicitudes subsecuentes se generarán sucesivamente a partir de estas solicitudes iniciales.

- `parse()`: un método que se llamará para manejar la respuesta descargada para cada una de las solicitudes realizadas. El parámetro de respuesta es una instancia de TextResponse que contiene el contenido de la página y tiene más métodos útiles para manejarlo.

El método `parse()` generalmente analiza la respuesta, extrae los datos raspados como diccionarios y también encuentra nuevas URL para seguir y crea nuevas solicitudes (Request) a partir de ellas.

## Cómo ejecutar nuestro spider

Para poner nuestro spider a trabajar, ve al directorio de nivel superior del proyecto y ejecuta:

```bash
scrapy crawl quotes
```

Este comando ejecuta el spider con el nombre "quotes" que acabamos de añadir, el cual enviará algunas solicitudes al dominio quotes.toscrape.com. Obtendrás una salida similar a esta:

```
... (omitido por brevedad)
2016-12-16 21:24:05 [scrapy.core.engine] INFO: Spider abierto
2016-12-16 21:24:05 [scrapy.extensions.logstats] INFO: Rastreadas 0 páginas (a 0 páginas/min), extraídos 0 elementos (a 0 elementos/min)
2016-12-16 21:24:05 [scrapy.extensions.telnet] DEBUG: Consola Telnet escuchando en 127.0.0.1:6023
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Rastreado (404) <GET https://quotes.toscrape.com/robots.txt> (referer: None)
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Rastreado (200) <GET https://quotes.toscrape.com/page/1/> (referer: None)
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Rastreado (200) <GET https://quotes.toscrape.com/page/2/> (referer: None)
2016-12-16 21:24:05 [quotes] DEBUG: Archivo guardado quotes-1.html
2016-12-16 21:24:05 [quotes] DEBUG: Archivo guardado quotes-2.html
2016-12-16 21:24:05 [scrapy.core.engine] INFO: Cerrando spider (terminado)
...
```

Ahora, verifica los archivos en el directorio actual. Deberías notar que se han creado dos archivos nuevos: quotes-1.html y quotes-2.html, con el contenido para las respectivas URL, según lo instruye nuestro método parse.


## ¿Qué ocurrió bajo el capó?

Scrapy programa los objetos `scrapy.Request` devueltos por el método `start_requests` del `Spider`. Al recibir una respuesta para cada uno, instancia objetos Response y llama al método de devolución de llamada asociado con la solicitud (en este caso, el método parse) pasando la respuesta como argumento.

## Un atajo para el método start_requests

En lugar de implementar un método `start_requests()` que genere objetos `scrapy.Requesta` partir de URLs, puedes simplemente definir un atributo de clase `start_urls` con una lista de URLs. Esta lista será utilizada por la implementación predeterminada de start_requests() para crear las solicitudes iniciales para tu spider.

```python
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
```
El método parse() será llamado para manejar cada una de las solicitudes para esas URL, aunque no hayamos indicado explícitamente a Scrapy que lo haga. Esto ocurre porque parse() es el método de devolución de llamada predeterminado de Scrapy, que se llama para solicitudes sin un método de devolución de llamada asignado explícitamente.

## Extracción de datos

La mejor manera de aprender cómo extraer datos con Scrapy es probando selectores usando el shell de Scrapy. Ejecuta:

```bash
scrapy shell 'https://quotes.toscrape.com/page/1/'
```

Nota

Recuerda siempre encerrar las URL entre comillas al ejecutar el shell de Scrapy desde la línea de comandos, de lo contrario, las URL que contengan argumentos (es decir, el carácter &) no funcionarán.

En Windows, usa comillas dobles en su lugar:

```
scrapy shell "https://quotes.toscrape.com/page/1/"
```

Usando el shell, puedes intentar seleccionar elementos usando CSS con el objeto de respuesta:

```python
response.css("title")
[<Selector query='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
```

El resultado de ejecutar response.css('title') es un objeto similar a una lista llamado SelectorList, que representa una lista de objetos Selector que envuelven elementos XML/HTML y te permiten ejecutar consultas adicionales para afinar la selección o extraer los datos.

Para extraer el texto del título anterior, puedes hacer:

```python
response.css("title::text").getall()
['Quotes to Scrape']
```

Hay dos cosas a tener en cuenta aquí: una es que hemos agregado ::text a la consulta de CSS, lo que significa que queremos seleccionar solo los elementos de texto directamente dentro del elemento `<title>`. Si no especificamos `::text`, obtendríamos el elemento de título completo, incluyendo sus etiquetas:

```python
response.css("title").getall()
['<title>Quotes to Scrape</title>']
```

La otra cosa es que el resultado de llamar a .getall() es una lista: es posible que un selector devuelva más de un resultado, así que los extraemos todos. Cuando sabes que solo quieres el primer resultado, como en este caso, puedes hacer:

```python
response.css("title::text").get()
'Quotes to Scrape'
```

Como alternativa, podrías haber escrito:

```python
response.css("title::text")[0].get()
'Quotes to Scrape'
```

Acceder a un índice en una instancia de SelectorList generará una excepción IndexError si no hay resultados:

```python
response.css("noelement")[0].get()
Traceback (most recent call last):
...
IndexError: list index out of range
```

Es posible que quieras usar .get() directamente en la instancia de SelectorList en su lugar, que devuelve None si no hay resultados:

```python
response.css("noelement").get()
```

Hay una lección aquí: para la mayoría del código de raspado, quieres que sea resistente a errores debido a que no se encuentren cosas en una página, para que incluso si algunas partes no se pueden extraer, al menos puedas obtener algunos datos.

Además de los métodos getall() y get(), también puedes usar el método re() para extraer usando expresiones regulares:

```python
response.css("title::text").re(r"Quotes.*")
['Quotes to Scrape']

response.css("title::text").re(r"Q\w+")
['Quotes']

response.css("title::text").re(r"(\w+) to (\w+)")
['Quotes', 'Scrape']
```

Para encontrar los selectores CSS adecuados para usar, puede ser útil abrir la página de respuesta desde el shell en tu navegador web usando view(response). Puedes usar las herramientas de desarrollo del navegador para inspeccionar el HTML y encontrar un selector (ver Uso de las herramientas de desarrollo del navegador para el raspado).

Selector Gadget también es una buena herramienta para encontrar rápidamente el selector CSS para elementos seleccionados visualmente, que funciona en muchos navegadores.

XPath: una breve introducción

Además de CSS, los selectores de Scrapy también admiten el uso de expresiones XPath:

```python
response.xpath("//title")
[<Selector query='//title' data='<title>Quotes to Scrape</title>'>]
```

```python
response.xpath("//title/text()").get()
'Quotes to Scrape'
```

Las expresiones XPath son muy poderosas y son la base de los Selectores de Scrapy. De hecho, los selectores CSS se convierten a XPath bajo el capó. Puedes ver esto si lees detenidamente la representación de texto de los objetos selector en el shell.

Aunque quizás no sean tan populares como los selectores CSS, las expresiones XPath ofrecen más potencia porque, además de navegar la estructura, también pueden examinar el contenido. Usando XPath, puedes seleccionar cosas como: seleccionar el enlace que contiene el texto "Siguiente página". Esto hace que XPath sea muy adecuado para la tarea de raspado, y te animamos a que aprendas XPath incluso si ya sabes cómo construir selectores CSS, hará que el raspado sea mucho más fácil.

Aquí no cubriremos mucho de XPath, pero puedes leer más sobre el uso de XPath con Selectores de Scrapy aquí. Para aprender más sobre XPath, te recomendamos este tutorial para aprender XPath a través de ejemplos, y este tutorial para aprender "cómo pensar en XPath".

## Extraer citas y autores

Ahora que sabes un poco sobre la selección y extracción, vamos a completar nuestro spider escribiendo el código para extraer las citas de la página web.

Cada cita en https://quotes.toscrape.com está representada por elementos HTML que se ven así:

```html
<div class="quote">
    <span class="text">“The world as we have created it is a process of our
    thinking. It cannot be changed without changing our thinking.”</span>
    <span>
        by <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
    </span>
    <div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
    </div>
</div>
```

Abramos el shell de scrapy y juguemos un poco para descubrir cómo extraer los datos que queremos:

```bash
scrapy shell 'https://quotes.toscrape.com'
```

Obtenemos una lista de selectores para los elementos HTML de cita con:

```python
response.css("div.quote")
[<Selector query="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>,
<Selector query="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>,
...]
```

Cada uno de los selectores devueltos por la consulta anterior nos permite ejecutar consultas adicionales sobre sus subelementos. Asignemos el primer selector a una variable, para que podamos ejecutar nuestros selectores CSS directamente en una cita en particular:

```python
quote = response.css("div.quote")[0]
```

Ahora, extraigamos el texto, el autor y las etiquetas de esa cita usando el objeto de cita que acabamos de crear:

```python
text = quote.css("span.text::text").get()

text
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'

author = quote.css("small.author::text").get()

author
'Albert Einstein'

Dado que las etiquetas son una lista de cadenas, podemos usar el método .getall() para obtener todas ellas:

```python
tags = quote.css("div.tags a.tag::text").getall()

tags
['change', 'deep-thoughts', 'thinking', 'world']
```

Habiendo descubierto cómo extraer cada parte, ahora podemos iterar sobre todos los elementos de citas y juntarlos en un diccionario de Python:

```python
for quote in response.css("div.quote"):

    text = quote.css("span.text::text").get()

    author = quote.css("small.author::text").get()

    tags = quote.css("div.tags a.tag::text").getall()

    print(dict(text=text, author=author, tags=tags))


{'text': '“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”', 'author': 'Albert Einstein', 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
{'text': '“It is our choices, Harry, that show what we truly are, far more than our abilities.”', 'author': 'J.K. Rowling', 'tags': ['abilities', 'choices']}
...
```


## Extracción de datos en nuestro spider

Volviendo a nuestro spider. Hasta ahora, no extrae ningún dato en particular, simplemente guarda toda la página HTML en un archivo local. Vamos a integrar la lógica de extracción anterior en nuestro spider.

Un spider de Scrapy típicamente genera muchos diccionarios que contienen los datos extraídos de la página. Para hacer eso, usamos la palabra clave yield de Python en el callback, como puedes ver a continuación:

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
```

Para ejecutar este spider, sal del shell de scrapy ingresando:

```bash
quit()
```

Luego, ejecuta:

```bash
scrapy crawl quotes
```

Ahora, debería mostrar los datos extraídos con el registro:

```bash
2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Extraído de <200 https://quotes.toscrape.com/page/1/>
{'tags': ['life', 'love'], 'author': 'André Gide', 'text': '“It is better to be hated for what you are than to be loved for what you are not.”'}
2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Extraído de <200 https://quotes.toscrape.com/page/1/>
{'tags': ['edison', 'failure', 'inspirational', 'paraphrased'], 'author': 'Thomas A. Edison', 'text': "“I have not failed. I've just found 10,000 ways that won't work.”"}
```

## Almacenar los datos extraídos

La forma más simple de almacenar los datos extraídos es usando la exportación de feeds, con el siguiente comando:

```bash
scrapy crawl quotes -O quotes.json
```

Esto generará un archivo quotes.json que contendrá todos los elementos extraídos, serializados en JSON.

El modificador -O en la línea de comandos sobrescribe cualquier archivo existente; usa -o en su lugar para añadir nuevo contenido a cualquier archivo existente. Sin embargo, agregar a un archivo JSON hace que el contenido del archivo sea JSON no válido. Cuando agregas a un archivo, considera usar un formato de serialización diferente, como JSON Lines:

```bash
scrapy crawl quotes -o quotes.jsonl
```

El formato JSON Lines es útil porque es similar a un flujo, puedes añadir fácilmente nuevos registros a él. No tiene el mismo problema de JSON cuando se ejecuta dos veces. Además, como cada registro es una línea separada, puedes procesar archivos grandes sin tener que ajustar todo en memoria, existen herramientas como JQ para ayudar a hacer eso en la línea de comandos.

En proyectos pequeños (como el de este tutorial), eso debería ser suficiente. Sin embargo, si deseas realizar cosas más complejas con los elementos extraídos, puedes escribir un Pipeline de Items. Se ha configurado un archivo de marcador de posición para los Pipelines de Items para ti cuando se crea el proyecto, en tutorial/pipelines.py. Aunque no necesitas implementar ningún pipeline de items si solo quieres almacenar los elementos extraídos.



## Siguiendo enlaces

Digamos que, en lugar de simplemente raspar el contenido de las dos primeras páginas de https://quotes.toscrape.com, quieres citas de todas las páginas del sitio web.

Ahora que sabes cómo extraer datos de las páginas, veamos cómo seguir enlaces desde ellas.

Lo primero es extraer el enlace a la página que queremos seguir. Examinando nuestra página, podemos ver que hay un enlace a la página siguiente con el siguiente marcado:

```html
<ul class="pager">
    <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
    </li>
</ul>
```

Podemos intentar extraerlo en el shell:

```python
response.css('li.next a').get()
'<a href="/page/2/">Next <span aria-hidden="true">→</span></a>'
```

Esto obtiene el elemento de anclaje, pero queremos el atributo href. Para eso, Scrapy admite una extensión de CSS que te permite seleccionar el contenido del atributo, así:

```python
response.css("li.next a::attr(href)").get()
'/page/2/'
```

También hay una propiedad attrib disponible (ver Seleccionar atributos de elementos para más detalles):

```python
response.css("li.next a").attrib["href"]
'/page/2/'
```

Veamos ahora nuestro spider modificado para seguir recursivamente el enlace a la página siguiente, extrayendo datos de ella:

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
```

Ahora, después de extraer los datos, el método parse() busca el enlace a la página siguiente, construye una URL absoluta completa usando el método urljoin() (ya que los enlaces pueden ser relativos) y emite una nueva solicitud a la página siguiente, registrándose a sí mismo como devolución de llamada para manejar la extracción de datos de la próxima página y para mantener el rastreo continuo a través de todas las páginas.

Lo que ves aquí es el mecanismo de Scrapy para seguir enlaces: cuando emites una solicitud en un método de devolución de llamada, Scrapy programará esa solicitud para que se envíe y registrará un método de devolución de llamada para que se ejecute cuando esa solicitud se complete.

Usando esto, puedes construir rastreadores complejos que siguen enlaces según las reglas que defines, y extraer diferentes tipos de datos dependiendo de la página que está visitando.

En nuestro ejemplo, crea una especie de bucle, siguiendo todos los enlaces a la siguiente página hasta que no encuentre uno; útil para rastrear blogs, foros y otros sitios con paginación.



## Más ejemplos y patrones

Aquí hay otro araña que ilustra callbacks y el seguimiento de enlaces, esta vez para la extracción de información de los autores:

```python
import scrapy

class AuthorSpider(scrapy.Spider):
    name = "author"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        author_page_links = response.css(".author + a")
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        yield {
            "name": extract_with_css("h3.author-title::text"),
            "birthdate": extract_with_css(".author-born-date::text"),
            "bio": extract_with_css(".author-description::text"),
        }
```

Este araña comenzará desde la página principal, seguirá todos los enlaces a las páginas de los autores llamando al callback `parse_author` para cada uno de ellos, y también seguirá los enlaces de paginación con el callback `parse` como vimos antes.

Aquí estamos pasando callbacks a `response.follow_all` como argumentos posicionales para hacer el código más corto; también funciona para Request.

El callback `parse_author` define una función auxiliar para extraer y limpiar los datos de una consulta CSS y emite el diccionario Python con los datos del autor.

Otra cosa interesante que este araña demuestra es que, incluso si hay muchas citas del mismo autor, no necesitamos preocuparnos por visitar la misma página del autor varias veces. Por defecto, Scrapy filtra las solicitudes duplicadas a URL ya visitadas, evitando el problema de golpear los servidores demasiado debido a un error de programación. Esto se puede configurar mediante el ajuste `DUPEFILTER_CLASS`.

Con suerte, en este momento tienes una buena comprensión de cómo usar el mecanismo de seguir enlaces y callbacks con Scrapy.

Como otro ejemplo de araña que aprovecha el mecanismo de seguir enlaces, echa un vistazo a la clase CrawlSpider para un araña genérico que implementa un pequeño motor de reglas que puedes usar para escribir tus propios crawlers sobre él.

Además, un patrón común es construir un ítem con datos de más de una página, usando un truco para pasar datos adicionales a los callbacks.

El uso de argumentos de línea de comandos en las arañas de Scrapy te permite personalizar el comportamiento de la araña al ejecutarla. Puedes pasar argumentos a través de la opción `-a` cuando ejecutas la araña. Por ejemplo:

```bash
scrapy crawl quotes -O quotes-humor.json -a tag=humor
```

Estos argumentos se pasan al método `__init__` de la araña y se convierten en atributos de la araña de forma predeterminada.

En este ejemplo, el valor proporcionado para el argumento `tag` estará disponible a través de `self.tag` en la araña. Puedes utilizar esto para hacer que tu araña recupere solo citas con un tag específico, construyendo la URL en función del argumento proporcionado.

Aquí hay un ejemplo de cómo usar los argumentos de la araña en una araña de Scrapy:

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = "https://quotes.toscrape.com/"
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = url + "tag/" + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

Si pasas el argumento `tag=humor` a esta araña, notarás que solo visitará URLs del tag de humor, como https://quotes.toscrape.com/tag/humor.