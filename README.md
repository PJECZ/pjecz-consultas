# pjecz-consultas


## Creadores de la información de la sección Consultas

Toda la información pública del **Poder Judicial del Estado de Coahuila de Zaragoza** se puede obtener en su sitio web [www.pjecz.gob.mx](https://www.pjecz.gob.mx); lo cual representa miles de archivos y altas cantidades de _gigabytes_ en datos.

Los programas en este repositorio sirven para listar los archivos descargables, extraer meta-información de sus nombres y directorios, y crear archivos JSON que las páginas web del sitio utilicen en programas Javascript que se ejecutan en el navegador.

Luego, usando [RClone](https://rclone.org) los archivos descargables se suben a [Google Cloud Storage](https://cloud.google.com/storage).


## Esquema de funcionamiento

Próximamente.


## Instalación

Cree un entorno virtual en Python 3 e instale

    $ pip install click

Instale el comando **consultas**

    $ pip install --editable .

Ejecute para mostrar la ayuda

    $ consultas --help
