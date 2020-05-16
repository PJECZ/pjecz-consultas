import click
import configparser
import os
import subprocess
import sys
from listas.acuerdos import Acuerdos
from listas.edictos import Edictos
from listas.especiales import Especiales
from listas.sentencias import Sentencias
from tests.tests import Tests


class Config(object):

    def __init__(self):
        self.rama = ''
        self.fecha_por_defecto = ''
        self.profundidad = 0
        self.insumos_ruta = ''
        self.json_ruta = ''
        self.url_ruta_base = ''
        self.rclone_origen = ''
        self.rclone_destino = ''


pass_config = click.make_pass_decorator(Config, ensure=True)

listas = None


@click.group()
@click.option('--rama', default='tests', type=str, help='Acuerdos, Edictos, Especiales, Sentencias o tests')
@pass_config
def cli(config, rama):
    click.echo('Hola, ¡soy Consultas!')
    # Rama
    if not rama in ['Acuerdos', 'Edictos', 'Especiales', 'Sentencias', 'tests']:
        click.echo('ERROR: Rama no programada.')
        sys.exit(1)
    config.rama = rama
    # Configuración
    settings = configparser.ConfigParser()
    settings.read('settings.ini')
    try:
        config.fecha_por_defecto = settings['Global']['fecha_por_defecto']
        config.profundidad = int(settings[config.rama]['profundidad'])
        config.insumos_ruta = settings[config.rama]['insumos_ruta']
        config.json_ruta = settings[config.rama]['json_ruta']
        config.url_ruta_base = settings[config.rama]['url_ruta_base']
        config.rclone_origen = settings[config.rama]['rclone_origen']
        config.rclone_destino = settings[config.rama]['rclone_destino']
    except KeyError:
        click.echo('ERROR: Falta configuración en settings.ini')
        sys.exit(1)
    # Preparar la instancia listas, pasando la configuración
    global listas
    if config.rama == 'Acuerdos':
        listas = Acuerdos(config)
    elif config.rama == 'Edictos':
        listas = Edictos(config)
    elif config.rama == 'Especiales':
        listas = Especiales(config)
    elif config.rama == 'Sentencias':
        listas = Sentencias(config)
    elif config.rama == 'tests':
        listas = Tests(config)


@cli.command()
@pass_config
def mostrar(config):
    """ Mostrar en pantalla """
    click.echo('Voy a mostrar...')
    global listas
    try:
        listas.alimentar()
        click.echo(repr(listas))
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
def crear(config):
    """ Crear """
    click.echo('Voy a crear...')
    cambios_contador = 0
    global listas
    try:
        listas.alimentar()
        for lista in listas.listas:
            json_archivo = os.path.basename(lista.json_ruta)
            if lista.guardar_archivo_json():
                click.echo(f'Guardados {len(lista.archivos)} renglones en {json_archivo}.')
                cambios_contador += 1
            else:
                click.echo(f'Sin cambios en {json_archivo}.')
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    if cambios_contador:
        click.echo(f'Hubo que actualizar {cambios_contador} listas.')
    else:
        click.echo('No hay ningún cambio en todas las listas.')
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
def sincronizar(config):
    """ Sincronizar bajando desde Archivista y subiendo a Google Storage """
    click.echo('Voy a sincronizar...')
    cambios_contador = 0
    global listas
    try:
        listas.alimentar()
        for lista in listas.listas:
            # Bajar desde Archivista
            os.chdir(lista.insumos_ruta)
            relativa_ruta = lista.insumos_ruta[len(config.insumos_ruta) + 1:]
            directorio = os.path.basename(os.path.normpath(relativa_ruta))
            resultado = subprocess.call(f'echo rclone --progress sync "{config.rclone_origen}/{relativa_ruta}" "{directorio}"', shell=True)
            # Si hay cambios
            json_archivo = os.path.basename(lista.json_ruta)
            if lista.guardar_archivo_json():
                # Subir a Google Storage
                click.echo('Guardados {} renglones en {}.'.format(len(lista.archivos), json_archivo))
                resultado = subprocess.call(f'echo rclone --progress sync "{directorio}" "{config.rclone_destino}/{relativa_ruta}"', shell=True)
                resultado = subprocess.call(f'echo rclone --progress copy "{json_archivo}" "{config.rclone_destino}/{json_archivo}"', shell=True)
                cambios_contador += 1
            else:
                click.echo(f'Sin cambios en {json_archivo}.')
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    if cambios_contador:
        click.echo(f'Hubo que actualizar {cambios_contador} listas.')
    else:
        click.echo('No hay ningún cambio en todas las listas.')
        sys.exit(1)
    sys.exit(0)


cli.add_command(mostrar)
cli.add_command(crear)
cli.add_command(sincronizar)
