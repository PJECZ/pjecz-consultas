import os
import tabulate
from comun.lista import Lista


class Sentencia(Lista):
    """ Sentencia """

    def alimentar(self):
        """ Alimentar """
        super().alimentar()
        if self.alimentado == False:
            for item in self.archivos:
                # Separar .../autoridad/fecha-nnn-yyyy-nnn-yyyy-g.pdf
                archivo = os.path.basename(item.path)
                nombre = os.path.splitext(archivo)[0]
                relativa_ruta = item.path[len(self.insumos_ruta):]
                directorio = os.path.dirname(item.path)
                carpetas = directorio.split('/')
                separados = nombre[11:].split('-') # ['nnn', 'yyyy', 'nnn', 'yyyy', 'g']
                # Campos
                fecha = self.campo_fecha(nombre[:10])
                if len(separados) >= 4:
                    sentencia = self.campo_expediente(separados[0], separados[1])
                    expediente = self.campo_expediente(separados[2], separados[3])
                else:
                    sentencia = 'nnn/YYYY'
                    expediente = 'nnn/YYYY'
                if len(separados) > 4 and separados[4] == 'g':
                    p_genero = 'Sí'
                else:
                    p_genero = 'No'
                autoridad = self.campo_texto(carpetas[-1]) # Última carpeta
                url = self.campo_descargable(relativa_ruta)
                # Renglón
                renglon = {
                    'Fecha': fecha,
                    'Juzgado/Tribunal': autoridad,
                    'P. Género': p_genero,
                    'Sentencia': sentencia,
                    'Expediente': expediente,
                    'Archivo': url,
                    }
                # Acumular en la tabla
                self.tabla.append(renglon)
            # Ya está alimentado
            self.alimentado = True

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        if len(self.tabla) == 0:
            return(f'<Sentencia> {self.insumos_ruta} SIN ARCHIVOS')
        tabla = [[
            'Fecha',
            'Juzgado/Tribunal',
            'P. Género',
            'Sentencia',
            'Expediente',
            'Archivo',
            ]]
        for renglon in self.tabla:
            tabla.append([
                renglon['Fecha'],
                renglon['Juzgado/Tribunal'],
                renglon['P. Género'],
                renglon['Sentencia'],
                renglon['Expediente'],
                renglon['Archivo'],
                ])
        salida = []
        salida.append(f'<Sentencia> {self.insumos_ruta}')
        salida.append(tabulate.tabulate(tabla, headers='firstrow'))
        salida.append('Son {} renglones en {}.\n'.format(len(self.archivos), self.json_ruta))
        return('\n'.join(salida))
