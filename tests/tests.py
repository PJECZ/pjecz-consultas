import os
import tabulate
from comun.listas import Listas


class Tests(Listas):
    """ Pruebas """

    def alimentar(self):
        """ Alimentar la tabla con las columnas de Tests """
        super().alimentar()
        if self.alimentado == False:
            for item in self.archivos:
                archivo = os.path.basename(item.path)
                nombre = os.path.splitext(archivo)[0]
                fecha = self.validar_fecha(nombre[:10])
                autoridad = self.validar_autoridad(nombre[11:])
                url = self.validar_url(item.path)
                renglon = { 'Fecha': fecha, 'Juzgado': autoridad, 'Archivo': url }
                self.tabla.append(renglon)
            self.alimentado = True

    def __repr__(self):
        super().__repr__()
        tabla = [['Fecha', 'Juzgado', 'Archivo']]
        for renglon in self.tabla:
            tabla.append(renglon.values())
        salida = []
        salida.append('<Tests>')
        salida.append(tabulate.tabulate(tabla, headers='firstrow'))
        salida.append('Son {} archivos.'.format(len(self.archivos)))
        return('\n'.join(salida))
