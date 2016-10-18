COMPILACIÓN DE PROYECTOS CON HERRAMIENTA PYTHON

make.py [-h] -P PROJECT [-v PROJECT_VERSION] (-g | -l) [-p PATH] (-d | -r) [--no-cross-compile] [-D] [-m MAKE_PARAMS] [-c] [-i]

Opciones:
-P PROJECT, --project PROJECT : Proyecto a compilar
-p PATH, --path PATH : path a fuentes locales del proyecto a compilar (si no en arhivo de definiciones)
-v VERSION, --project-version VERSION : versión del proyecto que se desea compilar (si no se indica, compilará la última). Sólo aplica cuando se compile desde GIT
-h, --help : mostrar ayuda
-g, --git: descargar fuentes de GIT
-l, --local: copiar fuentes de directorios locales
-r, --release: compilación en modo RELEASE
-d, --debug: compilación en modo DEBUG
--no-cross-compile : compilar para x86
-D, --compile-deps: compilar dependencias
-m MAKE_PARAMS, --make-params MAKE_PARAMS : parámetros adicionales a pasar al MAKE final de cada proyecto (si implementado)
-c, --create-only : sólo crea el makefile, pero no lo ejecuta
-i, --install: además de compilar, ejecuta la instalación. Fallará si el target INSTALL no está definido para el proyecto.
-C, --clean-install-dir: borra el directorio final de instalación antes de compilar

A tener en cuenta:
* El proyecto a compilar siempre se compila desde las fuentes. Nunca se hace una compilación parcial.
* Si se compilan dependencias, éstas se compilan desde las fuentes, estén o no estén anteriormente compiladas.
* Si no se compilan dependencias y éstas no están previamente compiladas, el programa da error.
* Sólo se lleva a cabo un control de versiones entre dependencias al compilar desde GIT. Si se compila desde local se hará con lo que haya en cada directorio.
* La aplicación buscará las dependencias en la carpeta DEPLOY_DIR que se corresponda con el modo de compilación elegido. No buscará en carpetas DEPLY_DIR de otros modos.
* Pendiente: opción de descargar desde las fuentes los binarios compilados.


Hacer un proyecto compatible con esta aplicación:
1. El proyecto se identificará unívocamente con un nombre en minúsculas, que se corresponderá con el nombre de la carpeta local y el nombre del repositorio GIT donde se aloje.
2. El proyecto contendrá una carpeta mrt con los siguientes archivos:
  * project: Contiene el target (archivo principal resultado de la compilación) bajo la sección [PROVIDES], y las dependencias que tenga ese proyecto bajo la sección [DEPS], con los nombres de los proyectos de los que dependa.
  * makefile.template: Makefile de instalación para el proyecto. Esta plantilla debe admitir y utilizar si es necesario las siguientes variables:
	- BUILD_DIR: Directorio de compilación para todos los proyectos
	- DEPLOY_DIR: Directorio de instalación temporal para todos los proyectos
	- GCC_DIR: Directorio donde se encuentran los ejecutables del compilador (gcc, g++, ar...)
	- INSTALL_DIR: Directorio donde se encuentra la raíz del ROOTFS que se generará al final
	- MAKE_FLAGS: Flags a pasar al makefile final.
	Además, esta plantilla tendrá dos target PHONY obligatorios: build (para compilar) e install (para pasar los resultados a la carpeta del rootfs final).
3. Tras la ejecución de la compilación (target BUILD de la plantilla) se deberán haber dejado los resultados en DEPLOY_DIR/proyecto. La estructura de carpetas será DEPLOY_DIR/proyecto/lib, DEPLOY_DIR/proyecto/bin, DEPLOY_DIR/proyecto/sbin, DEPLOY_DIR/proyecto/etc..., según corresponda.


La plantilla contendrá una línea encabezada por # TARGETS:, con una lista separada por comas con las siguientes opciones: arm.release, arm.debug, x86.release, x86.debug. Estos targets indicarán para que modos de compilación es válida la plantilla.
En el caso del modo DEBUG, se usará la plantilla RELEASE si la primera no está disponible.

GIT:
En Git tendremos las siguientes ramas:
master: código fuente original para librerías, fuentes de terceros o proyectos específicos de un producto (con código ya en el nombre)
402: rama para proyectos de supervisión avanzada no específicos de producto
402_xx (ej 402_02): rama para código adaptado a productos específicos.

A la hora de compilar desde Git, el programa buscará la rama adecuada, partiendo de la más específica (402_xx) a la más general.

Las versiones se etiquetarán de la siguiente forma: RAMA/version-adaptación. Por ejemplo:
402/v1.0.0 -> Rama 402, versión original 1.0.0
402_02/v1.0.1-a -> Rama 402_02, versión original 1.0.1, con cambios de Merytronic (versión a)


Para compilar desde Codeblocks:
* En Project/Properties/Project Settings:
	- Activar Custom Makefile
	- Directorio de ejecución, el principal del proyecto.
* En Project/Build Options:
	- En Make Commands: poner el comando python (por ejemplo: /MRT_OS/SRC/project_compiler/make.py -P 400_libutils_cpp -l -r)
	
	
NOTA:
Existe la posibilidad de añadir otra sección en el archivo PROJECT, sección INSTALL_DEPS. Esta sección se utiliza para especificar las dependencias de la instalación (qué targets de instalación ejecutar antes del del proyecto). 
No obstante, sólo se usa en el proyecto rootfs, que no tiene DEPS. Antes de combinar DEPS e INSTALL_DEPS, probar bien, aunque no se recomienda.
