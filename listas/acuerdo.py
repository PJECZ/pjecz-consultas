import os
import tabulate
from comun.lista import Lista


class Acuerdo(Lista):
    """ Acuerdo """

    def alimentar(self):
        """ Alimentar """
        super().alimentar()
        if self.alimentado == False:
            for item in self.archivos:
                # Separar fecha-descripcion.pdf
                archivo = os.path.basename(item.path)
                nombre = os.path.splitext(archivo)[0]
                relativa_ruta = item.path[len(self.insumos_ruta):]
                # Campos
                fecha = self.campo_fecha(nombre[:10])
                descripcion = self.campo_texto(nombre[11:])
                url = self.campo_descargable(relativa_ruta)
                # Renglón
                renglon = { 'Fecha': fecha, 'Descripción': descripcion, 'Archivo': url }
                # Acumular en la tabla
                self.tabla.append(renglon)
            # Ya está alimentado
            self.alimentado = True

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        if len(self.tabla) == 0:
            return(f'<Lista de Acuerdos> {self.insumos_ruta} SIN ARCHIVOS')
        tabla = [['Fecha', 'Descripción', 'Archivo']]
        for renglon in self.tabla:
            tabla.append(renglon.values())
        salida = []
        salida.append(f'<Lista de Acuerdos> {self.insumos_ruta}')
        salida.append(tabulate.tabulate(tabla, headers='firstrow'))
        salida.append('Son {} renglones en {}.\n'.format(len(self.archivos), self.json_ruta))
        return('\n'.join(salida))
