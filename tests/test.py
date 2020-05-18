import os
import tabulate
from comun.lista import Lista


class Test(Lista):
    """ Test """

    def alimentar(self):
        """ Alimentar """
        super().alimentar()
        if self.alimentado == False:
            for item in self.archivos:
                # Separar AAAA-MM-DD-NNN-AAAA-NNN-AAAA-g.pdf
                archivo = os.path.basename(item.path)
                nombre = os.path.splitext(archivo)[0]
                separados = nombre.split('-')
                # Tomar la fecha
                fecha = self.campo_fecha(f'{separados[0]}-{separados[1]}-{separados[2]}')
                # Tomar la sentencia
                if len(separados) >= 5:
                    sentencia = self.campo_expediente(separados[3], separados[4])
                else:
                    sentencia = 'nnn/YYYY'
                # Tomar el expediente
                if len(separados) >= 7:
                    expediente = self.campo_expediente(separados[5], separados[6])
                else:
                    expediente = 'nnn/YYYY'
                # Tomar el género
                if len(separados) >= 8 and separados[7].lower() == 'g':
                    p_genero = 'Sí'
                else:
                    p_genero = 'No'
                # Tomar el URL del archivo descargable
                relativa_ruta = item.path[len(self.insumos_ruta):]
                url = self.campo_descargable(relativa_ruta)
                # Renglón
                renglon = {
                    'Fecha': fecha,
                    'Sentencia': sentencia,
                    'Expediente': expediente,
                    'P. Género': p_genero,
                    'Archivo': url,
                    }
                # Acumular en la tabla
                self.tabla.append(renglon)
            # Ya está alimentado
            self.alimentado = True

    def tabla_texto(self):
        """ Crear tabla para mostrar en la terminal """
        if self.alimentado == False:
            self.alimentar()
        tabla = [['Fecha', 'Sentencia', 'Expediente', 'P. Género']]
        for renglon in self.tabla:
            tabla.append([
                renglon['Fecha'],
                renglon['Sentencia'],
                renglon['Expediente'],
                renglon['P. Género'],
                ])
        return(tabulate.tabulate(tabla, headers='firstrow'))

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        if len(self.tabla) == 0:
            return('<Lista de Test> SIN ARCHIVOS en {}'.format(self.insumos_ruta))
        else:
            return('<Lista de Test> con {} renglones en {}'.format(len(self.tabla), os.path.basename(self.json_ruta)))
