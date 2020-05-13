import os


class Listas(object):
    """ Listas """

    def __init__(self, config):
        self.config = config
        self.directorios = []
        self.listas = []
        self.alimentado = False

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
