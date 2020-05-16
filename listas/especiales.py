from comun.listas import Listas
from listas.especial import Especial


class Especiales(Listas):
    """ Especiales """

    def alimentar(self):
        """ Alimentar """
        super().alimentar()
        if self.alimentado == False:
            for insumos_ruta in self.directorios:
                self.listas.append(Especial(
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
        salida.append(f'<Especiales> Profundidad: {self.config.profundidad}')
        for lista in self.listas:
            salida.append(repr(lista))
        return('\n'.join(salida))
