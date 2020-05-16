from comun.listas import Listas
from listas.acuerdo import Acuerdo


class Acuerdos(Listas):
    """ Acuerdos """

    def alimentar(self):
        """ Alimentar """
        super().alimentar()
        if self.alimentado == False:
            for insumos_ruta in self.directorios:
                self.listas.append(Acuerdo(
                    insumos_ruta=insumos_ruta,
                    json_ruta=self.json_ruta_para_lista(insumos_ruta),
                    url_ruta_base=self.url_ruta_base_para_lista(insumos_ruta),
                    ))
            # Ya está alimentado
            self.alimentado = True

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        salida = []
        salida.append('<Acuerdos>')
        for lista in self.listas:
            salida.append(repr(lista))
        return('\n'.join(salida))
