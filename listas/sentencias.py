from comun.listas import Listas
from listas.sentencia import Sentencia


class Sentencias(Listas):
    """ Sentencias """

    def alimentar(self):
        """ Alimentar """
        super().alimentar()
        if self.alimentado == False:
            for insumos_ruta in self.directorios:
                json_ruta = self.config.json_ruta + '/falta-definir-nombre.json'
                url_ruta_base = self.config.url_ruta_base + insumos_ruta[len(self.config.insumos_ruta):]
                self.listas.append(Sentencia(
                    insumos_ruta=insumos_ruta,
                    json_ruta=json_ruta,
                    url_ruta_base=url_ruta_base,
                    ))
            # Ya está alimentado
            self.alimentado = True

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        salida = []
        salida.append('<Sentencias>')
        for lista in self.listas:
            salida.append(repr(lista))
        return('\n'.join(salida))
