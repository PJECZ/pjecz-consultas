from comun.listas import Listas
from tests.test import Test


class Tests(Listas):
    """ Tests """

    def alimentar(self):
        """ Alimentar """
        super().alimentar()
        if self.alimentado == False:
            for item in self.directorios:
                json_ruta = self.config.json_ruta + '/falta-definir-nombre.json'
                self.listas.append(Test(insumos_ruta=item, json_ruta=json_ruta))
            self.alimentado = True

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        salida = []
        salida.append('<Tests>')
        for lista in self.listas:
            salida.append(repr(lista))
        return('\n'.join(salida))
