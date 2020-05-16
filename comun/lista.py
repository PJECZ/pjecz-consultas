import datetime
import os
import json
from comun.funciones import cambiar_texto_a_palabras_en_mayusculas
from urllib.parse import quote


class Lista(object):
    """ Lista """

    def __init__(self, insumos_ruta, json_ruta, url_ruta_base):
        self.insumos_ruta = insumos_ruta
        self.json_ruta = json_ruta
        self.url_ruta_base = url_ruta_base
        self.archivos = []
        self.tabla = []
        self.alimentado = False

    def campo_fecha(self, texto):
        """ Campo con fecha AAAA-MM-DD """
        try:
            datetime.datetime.strptime(texto, '%Y-%m-%d')
            return(texto)
        except ValueError:
            return('2020-01-01')

    def campo_texto(self, texto):
        """ Poner en mayúculas la primer letra de cada palabra y cambiar los guiones por espacios """
        return(cambiar_texto_a_palabras_en_mayusculas(texto))

    def campo_expediente(self, numero, ano):
        """ Campo con expediente NNN/AAAA """
        return(f'numero/ano')

    def campo_descargable(self, ruta):
        """ URL con codigos seguros, ejemplo espacio a %20 """
        return(quote(self.url_ruta_base + ruta, safe=':/'))

    def rastrear_archivos(self, ruta):
        """ De forma recursiva entrega todos los archivos en la ruta """
        if not os.path.exists(ruta) or not os.path.isdir(ruta):
            Exception('No existe el directorio dado a rastrear_archivos.')
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield from self.rastrear_archivos(item.path)
            else:
                yield item

    def alimentar(self):
        """ Alimentar el listado de archivos """
        if self.alimentado == False:
            for item in self.rastrear_archivos(self.insumos_ruta):
                self.archivos.append(item)

    def contenido_json(self):
        """ Entrega el contenido para hacer el archivo JSON """
        if self.alimentado == False:
            self.alimentar()
        if len(self.tabla) == 0:
            return('')
        salida = { "data": self.tabla }
        return(json.dumps(salida))

    def guardar_archivo_json(self):
        """ Guardar el contenido JSON en archivo, entrega verdadero si hubo cambios """
        se_debe_guardar = False
        if os.path.exists(self.json_ruta):
            contenido = self.contenido_json()
            if contenido == '':
                return(False) # No hay archivos
            with open(self.json_ruta, 'r') as puntero:
                se_debe_guardar = contenido != puntero.read() # Si es diferente da verdadero
        else:
            se_debe_guardar = True # No existe
        if se_debe_guardar:
            with open(self.json_ruta, 'w') as puntero:
                puntero.write(self.contenido_json())
            return(True) # Si hubo cambios y guardó el archivo JSON
        else:
            return(False) # No hay cambios

    def __repr__(self):
        return('<Lista>')
