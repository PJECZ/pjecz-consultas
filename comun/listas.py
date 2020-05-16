import os
from comun.funciones import cambiar_texto_a_identificador


class Listas(object):
    """ Listas """

    def __init__(self, config):
        self.config = config
        self.directorios = []
        self.listas = []
        self.alimentado = False

    def json_ruta_para_lista(self, insumos_ruta):
        """ Entregar la ruta donde guardar el archivo JSON para una lista """
        if insumos_ruta == self.config.insumos_ruta:
            nombre = cambiar_texto_a_identificador(self.config.rama)
        else:
            nombre = cambiar_texto_a_identificador(insumos_ruta[len(self.config.insumos_ruta):])
        return(f"{self.config.json_ruta}/{nombre}.json")

    def url_ruta_base_para_lista(self, insumos_ruta):
        """ Entregar la URL base para las descargas de una lista """
        return(self.config.url_ruta_base + insumos_ruta[len(self.config.insumos_ruta):])

    def rastrear_directorios(self, ruta):
        """ Obtener todos los directorios en la ruta """
        if not os.path.exists(ruta) or not os.path.isdir(ruta):
            Exception('No existe el directorio dado a rastrear_directorios.')
        directorios = []
        with os.scandir(ruta) as scan:
            for item in scan:
                if item.is_dir():
                    directorios.append(item.path)
        return(directorios)

    def alimentar(self):
        """ Alimentar el listado de archivos """
        if self.alimentado == False:
            if self.config.profundidad == 2:
                for item in self.rastrear_directorios(self.config.insumos_ruta):
                    self.directorios.extend(self.rastrear_directorios(item))
            elif self.config.profundidad == 1:
                self.directorios = self.rastrear_directorios(self.config.insumos_ruta)
            elif self.config.profundidad == 0:
                self.directorios = [self.config.insumos_ruta]
            else:
                Exception('Profundidad incorrecta.')

    def __repr__(self):
        return('<Listas>')
