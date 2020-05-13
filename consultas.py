import click
import configparser
import sys
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


pass_config = click.make_pass_decorator(Config, ensure=True)

listas = None


@click.group()
@click.option('--rama', default='tests', type=str, help='Rama a procesar')
@pass_config
def cli(config, rama):
    click.echo('Hola, ¡soy Consultas!')
    # Rama
    if rama != 'Especiales' and rama != 'Sentencias' and rama != 'tests':
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
    except KeyError:
        sys.exit('ERROR: Falta configuración en settings.ini')
        sys.exit(1)
    # Preparar la instancia listas, pasando la configuración
    global listas
    if config.rama == 'Especiales':
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
    click.echo(repr(listas))
    sys.exit(0)


@cli.command()
@pass_config
def crear(config):
    """ Crear """
    click.echo('Voy a crear...')
    global listas
    if listas.guardar_archivo_json():
        click.echo(f'Se guardó {config.json_ruta}')
        sys.exit(0)
    else:
        click.echo('No hay cambios.')
        sys.exit(1)


cli.add_command(mostrar)
cli.add_command(crear)
