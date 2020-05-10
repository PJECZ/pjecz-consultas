import click
import configparser
import sys
from listas.listas_especiales import ListasEspeciales
from tests.tests import Tests


class Config(object):

    def __init__(self):
        self.rama = ''
        self.insumos_ruta = ''
        self.json_ruta = ''
        self.url_ruta_base = ''
        self.fecha_por_defecto = ''


pass_config = click.make_pass_decorator(Config, ensure=True)

listas = None


@click.group()
@click.option('--rama', default='tests', type=str, help='Rama a procesar')
@pass_config
def cli(config, rama):
    click.echo('Hola, ¡soy Consultas!')
    # Rama
    config.rama = rama
    if config.rama != 'Listas Especiales' and config.rama != 'tests':
        sys.exit('Error: La rama no está programada.')
    # Configuración
    settings = configparser.ConfigParser()
    settings.read('settings.ini')
    try:
        config.fecha_por_defecto = settings['Global']['fecha_por_defecto']
        config.insumos_ruta = settings[config.rama]['insumos_ruta']
        config.json_ruta = settings[config.rama]['json_ruta']
        config.url_ruta_base = settings[config.rama]['url_ruta_base']
    except KeyError:
        sys.exit('Falta configuración en settings.ini')
    # Preparar la varable listas
    global listas
    if config.rama == 'Listas Especiales':
        listas = ListasEspeciales(config)
    elif config.rama == 'tests':
        listas = Tests(config)


@cli.command()
@pass_config
def mostrar(config):
    """ Mostrar en pantalla """
    click.echo('Voy a mostrar...')
    global listas
    click.echo(repr(listas))
    sys.exit(0)


@cli.command()
@pass_config
def crear(config):
    """ Crear """
    click.echo('Voy a crear...')
    global listas
    click.echo(listas.guardar_archivo_json())
    sys.exit(0)


cli.add_command(mostrar)
cli.add_command(crear)
