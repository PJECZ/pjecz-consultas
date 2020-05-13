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


## Pasos de las Notarías para el envío de las Versiones Públicas de Edictos

Se solicita de la manera más atenta acatar los siguientes pasos:

1.- Convertir el edicto a un **archivo PDF**
2.- Cambiar el **nombre del archivo** de esta forma:

    - Fecha de publicación de la formato AAAA-MM-DD (año-mes-día), ejemplo: 2020-05-18.
    - Número de expediente con formato NNN-AAAA (número-año), ejemplo: 1234-2020.
    - Número de edicto con formato NNN-AAAA (número-año), ejemplo: 5678-2020.
    - Texto que ayude a identificar el archivo, como el tipo de acto. En minúsculas, sin espacios, sin acentos y separados por guiones medios (-), ejemplo: maria-lopez-garcia

**Ejemplo completo:** fecha del 28 de mayo 2020, expediente 1234/2020, edicto 5678/2020 y texto "María López García":

    2020-05-28-1234-2020-5678-2020-maria-lopez-garcia.pdf

    Observe que cada dato se separa por guiones medios (-) y que NUNCA debe usar el carácter de diagonal (/) ni caracteres extraños.

3.- Abra el **correo electrónico registrado de la Notaría.** El sistema clasifica el mensaje con su remitente. Si usa una cuenta distinta, se clasificará como NO identificado.
4.- En el asunto escriba:

    - Distrito
    - Notaría Número NN

5.- Adjuntar el archivo PDF
6.- Enviar a <edictos@pjec.gob.mx>.

**NOTA IMPORTANTE:** Todos los datos son de suma importancia. Los errores u omisiones en los nombres de los documentos PDF pueden dificultar su clasificación y búsqueda.


