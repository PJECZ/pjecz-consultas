import os
import tabulate
from comun.funciones import validar_autoridad, validar_fecha, validar_url
from comun.lista import Lista


class Test(Lista):
    """ Test """

    def alimentar(self):
        """ Alimentar """
        super().alimentar()
        if self.alimentado == False:
            for item in self.archivos:
                # Separar fecha-autoridad.pdf
                archivo = os.path.basename(item.path)
                nombre = os.path.splitext(archivo)[0]
                # Renglón
                fecha = validar_fecha(nombre[:10])
                autoridad = validar_autoridad(nombre[11:])
                url = validar_url(item.path)
                renglon = { 'Fecha': fecha, 'Juzgado': autoridad, 'Archivo': url }
                # Acumular en la tabla
                self.tabla.append(renglon)
            self.alimentado = True

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        tabla = [['Fecha', 'Juzgado', 'Archivo']]
        for renglon in self.tabla:
            tabla.append(renglon.values())
        salida = []
        salida.append(f'<Test> {self.insumos_ruta}')
        salida.append(tabulate.tabulate(tabla, headers='firstrow'))
        salida.append('Son {} archivos.'.format(len(self.archivos)))
        return('\n'.join(salida))
