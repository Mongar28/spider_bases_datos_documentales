import json
import requests
import re


def obtener_datos(url):
    cookies = {
        '__utma': '230685855.1690698426.1708373587.1709580237.1709606389.8',
        '__utmz': '230685855.1709242352.6.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        '_ga_PG5DW8YGFY': 'GS1.1.1709606389.7.1.1709606584.0.0.0',
        '_ga': 'GA1.1.641471803.1709219430',
        'popupClosed': 'true',
        'JSESSIONID': '0000kzGA6gB7H0JlarDld4N4nNM:17dh3et6h',
        '__utmb': '230685855.4.10.1709606389',
        '__utmc': '230685855',
        '__utmt': '1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Referer': 'https://www.redalyc.org/busquedaArticuloFiltros.oa?q=Ciencias%20sociales%20computacionales',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    response = requests.get(url, cookies=cookies, headers=headers)
    response.encoding = 'utf-8'  # Establecer la codificación
    data = response.json()["resultados"]

    return data


def escribir_json(data, filename='articulos_redalyc.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    datos_articulos_json = 'articulos_redalyc.json'

    # Crear el archivo JSON vacío
    escribir_json([])

    paginacion = 1

    while True:
        url = f'https://www.redalyc.org/service/r2020/getArticles/Ciencias%20sociales%20computacionales/{paginacion}/10/1/default'
        data = obtener_datos(url)

        if not data:
            break

        # Leer los datos existentes del archivo JSON
        try:
            with open(datos_articulos_json, 'r', encoding='utf-8') as f:
                datos_existente = json.load(f)
        except FileNotFoundError:
            datos_existente = []

        for item in data:
            resumen = item.get("resumen", "").replace(
                "\r", "").replace("\n", "")
            if resumen:
                resumen = resumen.split('>>>')[0]

            ruta_pdf = item.get("rutaArchivo", "")

            # Expresión regular para extraer el número
            expresion_regular = r'\\{1,2}(\d+)\.pdf'

            num_pdf = re.search(expresion_regular, ruta_pdf)
            num_pdf = num_pdf.group(1)

            link_descarga = f'https://www.redalyc.org/articulo.oa?id={num_pdf}'
            extracted_item = {
                "titulo": item.get("titulo", "").replace("\n", "").replace("\r", ""),
                "año": item.get("anioArticulo", ""),
                "autores": item.get("autores", "").replace("\n", "").replace("\r", ""),
                "revista": item.get("nomRevista", "").replace("\n", "").replace("\r", ""),
                "palabras": item.get("palabras", "").replace("\n", "").replace("\r", ""),
                "resumen": resumen,
                "link": link_descarga
            }

            datos_existente.append(extracted_item)

        escribir_json(datos_existente, datos_articulos_json)

        # reporte de proceso
        print("Reporte")
        print("*" * 100)
        print(f"---> Conteo de articulos scrapeados: {len(datos_existente)}")
        print(f"---> Paginación: {paginacion}")
        print("*" * 100)
        print("\n")

        paginacion += 1


if __name__ == "__main__":
    main()
