import os
#PROJECT_COMPILER_PROPERTIES
# Directorio de fuentes python
MAIN_DIR='/MRT_OS/SRC/project_compiler/'

#GLOBAL PROJECT VARIABLES
# Nombre del proyecto a generar
GLOBAL_PROJECT = ''

# Rama especifica del proyecto en GIT
GLOBAL_PROJECT_GIT_BRANCH = ''

#DIRECTORIES
# Directorios donde buscar codigos fuente de los proyectos a compilar
SRC_DIR = ('/MRT_OS/SRC/','/home/jonathan/Dropbox/CodeBlocks/')

# Directorios de trabajo para arm.release
BUILD_DIR = os.getcwd() + '/BUILD/'
DEPLOY_DIR = os.getcwd() + '/DEPLOY/'

# Directorios de trabajo para x86.release
BUILD_DIR_x86 = BUILD_DIR + 'x86/'
DEPLOY_DIR_x86 = DEPLOY_DIR + 'x86/'

# Directorios de trabajo para arm.debug
BUILD_DIR_DEBUG = os.getcwd() + '/BUILD_DEBUG/'
DEPLOY_DIR_DEBUG = os.getcwd() + '/DEPLOY_DEBUG/'

# Directorios de trabajo para x86.debug
BUILD_DIR_x86_DEBUG = BUILD_DIR_DEBUG + 'x86/'
DEPLOY_DIR_x86_DEBUG = DEPLOY_DIR_DEBUG + 'x86/'

#FINAL INSTALLATION DIRS
# Directorios de instalacion y de generacion de rootfs
INSTALL_DIR_GENERIC = os.getcwd() + '/SYSTEM/'
INSTALL_DIR_TFTP = os.getcwd() + '/SYSTEM_TFTP/'
INSTALL_DIR_FULL = os.getcwd() + '/SYSTEM_FULL/'
INSTALL_DIR_INCR = os.getcwd() + '/SYSTEM_INCR/'
ROOTFS_DIR = os.getcwd() + '/SYSTEM_IMAGE/'
RELEASES_DIR = os.getcwd() + '/RELEASES/'

QOS_FW_NAME = 'qos_fw.tar.xz'

#DATABASE PREFIX
DB_TABLES_PREFIX = ''

#TOOLCHAIN
# Directorios del toolchain para arm
GCC_LINK = '/MRT_OS/gcc-linaro-toolchain'
GCC_5_DIR = '/MRT_OS/gcc-linaro-toolchain-5/'
GCC_7_DIR = '/MRT_OS/gcc-linaro-toolchain-7.2.1/'
GCC_DIR = '/MRT_OS/gcc-linaro-toolchain/bin/'
#GCC_BIN_VERSION = '/MRT_OS/gcc-linaro-toolchain/bin/arm-linux-gnueabihf-gcc-7.2.1'
GCC_BIN_VERSION = GCC_DIR + '/arm-linux-gnueabihf-gcc'

# Directorios del toolchain para x86
GCC_DIR_x86 = '/usr/bin/'
GCC_BIN_x86_VERSION = '/usr/bin/gcc'

# Propiedades de GIT
GIT_URL = 'ssh://git@gitlab.merytronicidi.com:30022'
# Orden de busqueda de ramas
GIT_BRANCHES = ('', '402_12', '402', 'master')
# Namespaces de busqueda en git
GIT_NAMESPACES = ('mrt_developers', 'mrt_os_projects', 'general-libraries') 


BUILD_TYPE_FULL_MAINSH_TEMPLATE = "/mrt/templates/full_update/main.sh"
BUILD_TYPE_INCR_MAINSH_TEMPLATE = "/mrt/templates/incr_update/main.sh"

UBOOT_FILES = ["MLO", "u-boot.img"]

MRT_SERVER_FOLDER = "/media/merytronic/I+D\ PRODUCTOS/402\ -\ SABT/402.12\ \(ADVANCED\ FEEDER\ CONCENTRATOR\)/FIRMWARE/"


#DO NOT EDIT:
# Templates search order
templates = {'arm': {'debug': ('makefile.template.debug', 'makefile.template',), 'release' : ('makefile.template',)},
			'x86': {'debug': ('makefile.template.debug.x86', 'makefile.template.debug', 'makefile.template',), 'release': ('makefile.template.x86', 'makefile.template',)}}
			
build_paths = {'arm': {'debug': BUILD_DIR_DEBUG, 'release' : BUILD_DIR},
			'x86': {'debug': BUILD_DIR_x86_DEBUG, 'release': BUILD_DIR_x86}}
			
deploy_paths = {'arm': {'debug': DEPLOY_DIR_DEBUG, 'release' : DEPLOY_DIR},
			'x86': {'debug': DEPLOY_DIR_x86_DEBUG, 'release': DEPLOY_DIR_x86}}

GENERIC_MAKEFILE = "Makefile"
BUILD_TYPE_TFTP = 0
TFTP_BUILD_MAKEFILE = "Makefile_tftp"
BUILD_TYPE_FULL = 1
FULL_BUILD_MAKEFILE = "Makefile_full"
BUILD_TYPE_INCR = 2
INCR_BUILD_MAKEFILE = "Makefile_incr"

ROOTFS_PROJECT = "rootfs"
UBOOT_PROJECT = "u-boot"
CMM_PROJECT = "402_00_cmm_cpp"
CMM_PRIV_KEY_FILE = "/etc/cert_priv/fw_key.pem"
CMM_PUB_KEY_FILE = "/etc/cert/fw_key_pub.pem"

ARM_TEMPLATE_SUFFIX = "arm"
X86_TEMPLATE_SUFFIX = "x86"
RELEASE_TEMPLATE_SUFFIX = "release"
DEBUG_TEMPLATE_SUFFIX = "debug"

MAKEFILE_HEADER_TEMPLATE_FILE = "/templates/makefile_hdr.tmpl"
MAKEFILE_BUILD_TARGET_TEMPLATE_FILE = "/templates/build_target.tmpl"
MAKEFILE_INSTALL_TARGET_TEMPLATE_FILE = "/templates/install_target.tmpl"
MAKEFILE_PHONY_TARGET_TEMPLATE_FILE = "/templates/phony_target.tmpl"
MAKEFILE_IMAGE_TARGET_TEMPLATE_FILE = "/templates/image_target.tmpl"
MAKEFILE_INCR_TARGET_TEMPLATE_FILE = "/templates/incr_install.tmpl"


PROJECT_UPDATE_BASE = "/mrt/incr_update/"

''' Archivo con los comandos a ejecutar en una actualizacion incremental
previos a la copia de archivos a /sabt y a / 
	Son especificos para cada nueva version de proyecto
'''
PROJECT_UPDATE_PRE_CMDS_FILE = "pre_cmds.tmpl"

''' Archivo con los comandos a ejecutar en una actualizacion incremental
posteriores a la copia de archivos a /sabt y a / 
	Son especificos para cada nueva version de proyecto
'''
PROJECT_UPDATE_POST_CMDS_FILE = "post_cmds.tmpl"

''' Archivo con la lista de archivos extra copiar para llevar a cabo 
una actualizacion incremental de un proyecto.
Estos archivos seran usados por los scripts pre y post, y son independientes
de los propios archivos de instalacion del proyecto, que se copiaran
siempre
	Son especificos para cada nueva version de proyecto
'''
PROJECT_UPDATE_EXTRA_FILES_FILE = "files"
PROJECT_UPDATE_EXTRA_FILES_PATH = ""

MAINSH_FILE = "main.sh"

DB_HOST = "192.168.77.4"
DB_USER = "merytronic"
DB_PWD = "merytronic2012"
DB_NAME = "402_12_fw"

VALID_PART_NUMBERS = ("402.12.00", "402.12.01", "402.12.02", "402.12.03",
					"402.12.04", "402.12.05.01", "402.12.06", "402.12.07",)

VALID_FW_FAMILY = ("IBD", "UFD", "MLY", "MRT")

PRODUCT = "402.12"

FW_FAMILY_CODES = {'IBD':'001','UFD':'004','MRT':'000','MLY':'005'}


def set_GLOBAL_PROJECT(pn_list, fw_family, min_versions):
	global GLOBAL_PROJECT			#Now represents FW_FAMILY
	global GLOBAL_PROJECT_GIT_BRANCH
	global DB_TABLES_PREFIX
	global GIT_BRANCHES
	
	if fw_family != "NULL" and fw_family not in VALID_FW_FAMILY:
		print "Error fw-family", fw_family, "not allowed"
		exit(1)
			
	if min_versions != "local":
		for min_vers in min_versions.split(";"):
			if min_vers.split(",")[0] not in VALID_FW_FAMILY:
				print "Error fw-family", min_vers.split(",")[0], "not allowed for minimal version"
				exit(1)
	
	GLOBAL_PROJECT = fw_family
	GLOBAL_PROJECT_GIT_BRANCH = fw_family
	GIT_BRANCHES = (GLOBAL_PROJECT_GIT_BRANCH, '402_12', '402', 'master')

