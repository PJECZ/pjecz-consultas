import click
import sys
from listas_especiales.listas_especiales import ListasEspeciales
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
@click.option('--rama', default='Listas Especiales', type=str, help='Rama a procesar')
@pass_config
def cli(config, rama):
    click.echo('Hola, ¡soy Consultas!')
    config.rama = rama
    if config.rama == 'Listas Especiales':
        from listas_especiales.settings import insumos_ruta, json_ruta, url_ruta_base, fecha_por_defecto
    elif config.rama == 'tests':
        from tests.settings import insumos_ruta, json_ruta, url_ruta_base, fecha_por_defecto
    else:
        sys.exit('Error: La rama no está programada.')
    config.insumos_ruta = insumos_ruta
    config.json_ruta = json_ruta
    config.url_ruta_base = url_ruta_base
    config.fecha_por_defecto = fecha_por_defecto
    click.echo(f'  Insumos ruta:      {config.insumos_ruta}')
    click.echo(f'  JSON ruta:         {config.json_ruta}')
    click.echo(f'  URL ruta base:     {config.url_ruta_base}')
    click.echo(f'  Fecha por defecto: {config.fecha_por_defecto}')
    global listas
    if (config.rama == 'Listas Especiales'):
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
