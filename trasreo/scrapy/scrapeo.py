import requests
from lxml import html

# URL de la página de búsqueda
url = 'https://www.redalyc.org/busquedaArticuloFiltros.oa?q=desarrollo%20social'

# Descargar el HTML de la página
response = requests.get(url)
html_content = response.content

# Parsear el HTML
tree = html.fromstring(html_content)

# Extraer títulos de los artículos y sus enlaces utilizando selectores CSS
articles = tree.cssselect('.title')

# Imprimir los títulos y enlaces
for article in articles:
    # Extraer el texto del título y limpiarlo
    title_text = article.text_content().strip()
    # Extraer el enlace del artículo
    link = article.get('href')
    print("Título:", title_text)
    print("Enlace:", link)
    print()
