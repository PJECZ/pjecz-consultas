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
                separados = nombre.split('-')
                # Tomar la fecha
                if len(separados) >= 3:
                    fecha = self.campo_fecha(f'{separados[0]}-{separados[1]}-{separados[2]}')
                else:
                    fecha = '2000-01-01' # Fecha por defecto
                # Tomar la descripción
                if len(separados) >= 4:
                    descripcion = self.campo_texto(' '.join(separados[3:]))
                else:
                    descripcion = ''
                # Tomar el URL del archivo descargable
                relativa_ruta = item.path[len(self.insumos_ruta):]
                url = self.campo_descargable(relativa_ruta)
                # Renglón
                renglon = { 'Fecha': fecha, 'Descripción': descripcion, 'Archivo': url }
                # Acumular en la tabla
                self.tabla.append(renglon)
            # Ya está alimentado
            self.alimentado = True

    def tabla_texto(self):
        """ Crear tabla para mostrar en la terminal """
        tabla = [['Fecha', 'Descripción', 'Archivo']]
        for renglon in self.tabla:
            tabla.append(renglon.values())
        return(tabulate.tabulate(tabla, headers='firstrow'))

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        if len(self.tabla) == 0:
            return('<Lista de Acuerdos> SIN ARCHIVOS en {}'.format(self.insumos_ruta))
        else:
            return('<Lista de Acuerdos> con {} renglones en {}'.format(len(self.tabla), os.path.basename(self.json_ruta)))
