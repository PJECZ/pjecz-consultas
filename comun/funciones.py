import datetime
import os
import re
import unicodedata
from urllib.parse import quote


def cambiar_texto_a_sin_acentos(texto):
    """ A caracteres sin acentos """
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore')
    texto = texto.decode("utf-8")
    return(str(texto))

def cambiar_texto_a_ruta_segura(texto):
    """ A una ruta segura en minúsculas, espacios a guiones y sin caracteres acentuados, pero mantiene diagonales """
    texto = cambiar_texto_a_sin_acentos(texto.lower())
    texto = re.sub('[ ]+', '-', texto)
    texto = re.sub('[^0-9a-zA-Z_/-]', '', texto)
    return(texto)

def cambiar_texto_a_identificador(texto):
    """ A identificador en minúsculas, espacios a guiones y sin caracteres acentuados """
    texto = cambiar_texto_a_sin_acentos(texto.lower())
    texto = re.sub('[/]+', '-', texto)
    texto = re.sub('[ ]+', '-', texto)
    texto = re.sub('[^0-9a-zA-Z_-]', '', texto)
    return(texto)

def cambiar_texto_a_palabras_en_mayusculas(texto):
    """ El primer caracter de cada palabra en mayúscula, el resto en minúsculas, guiones a espacios """
    texto = re.sub('[-]+', ' ', texto)
    return(texto.title())

def validar_fecha(texto):
    """ Validar la fecha en formato año-mes-dia, si es incorrecta da la fecha por defecto """
    try:
        datetime.datetime.strptime(texto, '%Y-%m-%d')
        return(texto)
    except ValueError:
        return('2020-01-01')

def validar_autoridad(texto):
    """ Validar la autoridad """
    return(cambiar_texto_a_palabras_en_mayusculas(texto))

def validar_url(ruta):
    """ Validar la URL """
    #url = self.config.url_ruta_base + ruta[len(self.config.insumos_ruta):] # Cambia la parte igual a insumos_ruta por url_ruta_base
    url = 'https://fake.org.mx'
    url_seguro = quote(url, safe=':/') # URL con codigos seguros, ejemplo espacio a %20
    return(url_seguro)
