# Es una clase que se llama busqueda REA (Reconocimiento de Entidades Academicas)

from typing import Optional, List, Tuple
import re
from openai import OpenAI


class Rea:
    __api_key: Optional[str] = ''

    def __init__(self, api_key: Optional[str]) -> Optional[None]:
        self.__api_key = api_key
        print("Initialized")

    def extractor_obj(self, texto: Optional[str]) -> Optional[str]:
        client = OpenAI(api_key=self.__api_key)

        response = client.completions.create(model="gpt-3.5-turbo-instruct",
                                             prompt=f"Identifica la frase que expresa la acción central de la investigación en el siguiente objetivo general. sintetizala en una sola linea corta. No tengas en cuenta los topónimos. Tampoco tengas en cuenta  el 'cómo', 'la forma en que se hace', el 'mediante',  el 'para qué', el 'dónde', la 'temporalidad' , 'en lo que se basa'. Si aparece un territorio como pais, ciudad, minicipo,barrio, etc, no lo tengas en cuenta. Se concreto y responde solo lo que te pido. Solo basate en la información textual que te doy. Objetivo general: '{texto}'",
                                             max_tokens=1024,
                                             n=1,
                                             stop=None,
                                             temperature=0.9,
                                             top_p=1)

        respuesta = response.choices[0].text.strip()
        return respuesta

    def extractor_pob_tem(self, texto: Optional[str]) -> List[Tuple[str]]:
        client = OpenAI(api_key=self.__api_key)

        response = client.completions.create(model="gpt-3.5-turbo-instruct",
                                             prompt=f"Por favor, proporciona una lista de las siguientes entidades nombradas presentes en el texto: Grupos poblacionales, Territorios y Temporalidad. Los criterios que definen cada entidad son los siguientes: - Grupos poblacionales: Población, sujetos, actores, organizaciones, comunidades, Mujeres, obreros, campesinos, entre otras. -Territorios: Territorios, barrios, municipios, unidad administrativa, comunas, veredas, corregimientos, ciudades, países, entre otras unidades administrativas. -Temporalidad: Siglos, años, décadas, épocas, fechas, actualidad, todo lo relaciona al contexto temporal. Si no encuentras en el texto la entidad, entonces no devuelvas nada. Si hay varias entidades repetidas, igual ponlas cada una con su texto y entidad. Solo basate en lo que encuentres en el texto. Entrega por favor la respuesta con el texto y la entidad separados por comas dentro de paréntesis, donde el primer elemento sea el texto y en segundo elemento dentro del paréntesis sea la entidad. Tal cual como se muestra en el ejemplo: (Europeos,Grupos poblacionales)(Nuevo Mundo,Territorios)(1492-1640,Escalas temporales). Texto: '{texto}'",
                                             max_tokens=1024,
                                             n=1,
                                             stop=None,
                                             temperature=0.9,
                                             top_p=1)

        entities = response.choices[0].text.strip()
        # Utilizamos re.findall() para obtener todas las entidades dentro de paréntesis
        entities_list: List[str] = re.findall(r'\((.*?)\)', entities)
        lista_entidades: List[Tuple[str]] = [
            tuple(entidad.split(',')) for entidad in entities_list]
        return lista_entidades

    def extractor_met(self, texto: Optional[str]) -> Optional[str]:
        client = OpenAI(api_key=self.__api_key)

        response = client.completions.create(model="gpt-3.5-turbo-instruct",
                                             prompt=f"Extrae las entidades que hablen sobre la metodología y las técnicas de investigación de este texto. Solo basate en lo que hay en el texto. Si no encuentras entidades, que hablan sobre la metodología y las tecnicas no respondas nada. Entrega la respuesta en una cadena de texto donde cada entidad esté separada por punto y coma: '{texto}'",
                                             max_tokens=1024,
                                             n=1,
                                             stop=None,
                                             temperature=0.9,
                                             top_p=1)

        respuesta = response.choices[0].text.strip()
        return respuesta
