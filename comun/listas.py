import datetime
import json
import os
from comun.funciones import cambiar_texto_a_palabras_en_mayusculas
from urllib.parse import quote


class Listas(object):
    """ Listas """

    def __init__(self, config):
        self.config = config
        self.archivos = []
        self.tabla = []
        self.alimentado = False

    def validar_fecha(self, texto):
        """ Validar la fecha en formato año-mes-dia, si es incorrecta da la fecha por defecto """
        try:
            datetime.datetime.strptime(texto, '%Y-%m-%d')
            return(texto)
        except ValueError:
            return(self.config.fecha_por_defecto)

    def validar_autoridad(self, texto):
        """ Validar la autoridad """
        return(cambiar_texto_a_palabras_en_mayusculas(texto))

    def validar_url(self, ruta):
        """ Validar la URL """
        url = self.config.url_ruta_base + ruta[len(self.config.insumos_ruta):] # Cambia la parte igual a insumos_ruta por url_ruta_base
        url_seguro = quote(url, safe=':/') # URL con codigos seguros, ejemplo espacio a %20
        return(url_seguro)

    def rastrear(self, ruta):
        """ De forma recursiva entrega todos los archivos en la ruta """
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield from self.rastrear(item.path)
            else:
                yield item

    def alimentar(self):
        """ Alimentar el listado de archivos """
        if self.alimentado == False:
            if not os.path.exists(self.config.insumos_ruta) or not os.path.isdir(self.config.insumos_ruta):
                Exception('No existe el directorio insumos_ruta.')
            for item in self.rastrear(self.config.insumos_ruta):
                self.archivos.append(item)

    def contenido_json(self):
        """ Entrega el contenido para hacer el archivo JSON """
        if self.alimentado == False:
            self.alimentar()
        salida = { "data": self.tabla }
        return(json.dumps(salida))

    def guardar_archivo_json(self):
        """ Guardar el contenido JSON en archivo, entrega verdadero si hubo cambios """
        se_debe_guardar = False
        if os.path.exists(self.config.json_ruta):
            contenido = self.contenido_json()
            with open(self.config.json_ruta, 'r') as puntero:
                se_debe_guardar = contenido != puntero.read() # Si es diferente da verdadero
        else:
            se_debe_guardar = True # No existe
        if se_debe_guardar:
            with open(self.config.json_ruta, 'w') as puntero:
                puntero.write(self.contenido_json())
            return(True) # Si hubo cambios y guardó el archivo JSON
        else:
            return(False) # No hay cambios

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
