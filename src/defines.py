#PROJECT_COMPILER_PROPERTIES
# Directorio de fuentes python
MAIN_DIR='/MRT_OS/SRC/project_compiler/'

#GLOBAL PROJECT VARIABLES
# Nombre del proyecto a generar
GLOBAL_PROJECT = '402.02.alpha1'
# Rama especifica del proyecto en GIT
GLOBAL_PROJECT_GIT_BRANCH = '402_02'

#DIRECTORIES
# Directorios donde buscar codigos fuente de los proyectos a compilar
SRC_DIR = ('/MRT_OS/SRC/','/home/jonathan/Dropbox/CodeBlocks/')

# Directorios de trabajo para arm.release
BUILD_DIR = '/MRT_OS/402.02.alpha1/BUILD/'
DEPLOY_DIR = '/MRT_OS/402.02.alpha1/DEPLOY/'

# Directorios de trabajo para x86.release
BUILD_DIR_x86 = BUILD_DIR + 'x86/'
DEPLOY_DIR_x86 = DEPLOY_DIR + 'x86/'

# Directorios de trabajo para arm.debug
BUILD_DIR_DEBUG = '/MRT_OS/402.02.alpha1/BUILD_DEBUG/'
DEPLOY_DIR_DEBUG = '/MRT_OS/402.02.alpha1/DEPLOY_DEBUG/'

# Directorios de trabajo para x86.debug
BUILD_DIR_x86_DEBUG = BUILD_DIR_DEBUG + 'x86/'
DEPLOY_DIR_x86_DEBUG = DEPLOY_DIR_DEBUG + 'x86/'

#FINAL INSTALLATION DIRS
# Directorios de instalacion y de generacion de rootfs
INSTALL_DIR = '/MRT_OS/402.02.alpha1/SYSTEM/'
ROOTFS_DIR = '/MRT_OS/402.02.alpha1/SYSTEM_IMAGE/'


#TOOLCHAIN
# Directorios del toolchain para arm
GCC_DIR = '/MRT_OS/gcc-linaro-toolchain/bin/'
GCC_BIN_VERSION = '/MRT_OS/gcc-linaro-toolchain/bin/arm-linux-gnueabihf-gcc-4.9.2'

# Directorios del toolchain para x86
GCC_DIR_x86 = '/usr/bin/'
GCC_BIN_x86_VERSION = '/usr/bin/gcc'

# Propiedades de GIT
GIT_URL = 'git@gitlab.merytronic.com'
# Orden de busqueda de ramas
GIT_BRANCHES = (GLOBAL_PROJECT_GIT_BRANCH, '402', 'master')
# Namespaces de busqueda en git
GIT_NAMESPACES = ('mrt_developers', 'mrt_os_projects') 


#DO NOT EDIT:
# Templates search order
templates = {'arm': {'debug': ('makefile.template.debug', 'makefile.template',), 'release' : ('makefile.template',)},
			'x86': {'debug': ('makefile.template.debug.x86', 'makefile.template.debug', 'makefile.template',), 'release': ('makefile.template.x86', 'makefile.template',)}}
			
build_paths = {'arm': {'debug': BUILD_DIR_DEBUG, 'release' : BUILD_DIR},
			'x86': {'debug': BUILD_DIR_x86_DEBUG, 'release': BUILD_DIR_x86}}
			
deploy_paths = {'arm': {'debug': DEPLOY_DIR_DEBUG, 'release' : DEPLOY_DIR},
			'x86': {'debug': DEPLOY_DIR_x86_DEBUG, 'release': DEPLOY_DIR_x86}}
