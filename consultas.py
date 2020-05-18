import click
import configparser
import os
import shutil
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
    if not rama.title() in ['Acuerdos', 'Edictos', 'Especiales', 'Sentencias', 'Tests']:
        click.echo('ERROR: Rama no programada.')
        sys.exit(1)
    config.rama = rama.title()
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
    elif config.rama == 'Tests':
        listas = Tests(config)


@cli.command()
@pass_config
def mostrar(config):
    """ Mostrar en pantalla """
    click.echo('Voy a mostrar...')
    global listas
    try:
        listas.alimentar()
        for lista in listas.listas:
            click.echo(os.path.basename(lista.json_ruta))
            click.echo(lista.tabla_texto())
            click.echo()
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
                click.echo('Guardados {} renglones en {}'.format(len(lista.archivos), json_archivo))
                cambios_contador += 1
            else:
                click.echo(f'Sin cambios en {json_archivo}')
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    if cambios_contador:
        click.echo(f'Hubo que crear {cambios_contador} listas.')
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
            # Cuestión de directorios
            os.chdir(lista.insumos_ruta)
            if lista.insumos_ruta == config.insumos_ruta:
                directorio = os.path.basename(os.path.normpath(config.insumos_ruta))
                rclone_origen = config.rclone_origen
                rclone_destino = config.rclone_destino
            else:
                relativa_ruta = lista.insumos_ruta[len(config.insumos_ruta) + 1:]
                directorio = os.path.basename(os.path.normpath(relativa_ruta))
                rclone_origen = f'{config.rclone_origen}/{relativa_ruta}'
                rclone_destino = f'{config.rclone_destino}/{relativa_ruta}'
            # Bajar desde Archivista
            resultado = subprocess.call(f'rclone sync "{rclone_origen}" .', shell=True)
            # Si hay cambios en el archivo JSON
            json_archivo = os.path.basename(lista.json_ruta)
            if lista.guardar_archivo_json():
                # Subir a Google Storage
                click.echo('Guardados {} renglones en {}'.format(len(lista.archivos), json_archivo))
                shutil.copy(lista.json_ruta, 'lista.json')
                resultado = subprocess.call(f'rclone sync . "{rclone_destino}"', shell=True)
                cambios_contador += 1
            else:
                click.echo(f'Sin cambios en {json_archivo}')
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    if cambios_contador:
        click.echo(f'Hubo que sincronizar {cambios_contador} listas.')
    else:
        click.echo('No hay ningún cambio en todas las listas.')
        sys.exit(1)
    sys.exit(0)


cli.add_command(mostrar)
cli.add_command(crear)
cli.add_command(sincronizar)
