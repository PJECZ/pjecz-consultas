from comun.listas import Listas
from listas.especial import Especial


class Especiales(Listas):
    """ Especiales """

    def alimentar(self):
        """ Alimentar """
        super().alimentar()
        if self.alimentado == False:
            for item in self.directorios:
                json_ruta = self.config.json_ruta + '/falta-definir-nombre.json'
                self.listas.append(Especial(insumos_ruta=item, json_ruta=json_ruta))
            self.alimentado = True

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        salida = []
        salida.append('<Especiales>')
        for lista in self.listas:
            salida.append(repr(lista))
        return('\n'.join(salida))
