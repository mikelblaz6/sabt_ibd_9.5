import subprocess, sys, os, shutil

import local
import utils
import defines as constants

from utils import print_error



def do_make(file_path, target):
	p = subprocess.Popen(['make', '-f', file_path, target], close_fds = True)
	p.communicate()
	if p.returncode != 0:
		print_error("Error building " + file_path + ": " + target)
		raise Exception()


def do_build(project_tree, args, paths):
	
	for version in project_tree[args.project]:
		project_name = utils.get_full_path(args.project, version, args.compiler)
		break
	
	
	for project in project_tree:
		if args.project == project or args.compile_deps:
			for version in project_tree[project]:
				local.prepare_deploy(project, version, paths.deploy_path, args.compiler)
				break
	
	if args.images:
		do_make(paths.work_path + '/' + constants.TFTP_BUILD_MAKEFILE, project_name)
	else:
		do_make(paths.work_path + '/' + constants.GENERIC_MAKEFILE, project_name)
					
	print("------------- COMPILATION ENDED SUCCESSFULLY ----------------")
	

def do_install(project_tree, args, paths, build_type = None):
	for version in project_tree[args.project]:
		project_name = utils.get_full_path(args.project, version, args.compiler)
		break
	
	if build_type == constants.BUILD_TYPE_INCR:
		os.system("mkdir -p " + constants.INSTALL_DIR_INCR)
		do_make(paths.work_path + '/' + constants.INCR_BUILD_MAKEFILE, 'incr_release')
	else:
		if build_type == constants.BUILD_TYPE_TFTP:
			install_dir_name = constants.INSTALL_DIR_TFTP
			makefile_name = constants.TFTP_BUILD_MAKEFILE
		elif build_type == constants.BUILD_TYPE_FULL:
			install_dir_name = constants.INSTALL_DIR_FULL
			makefile_name = constants.FULL_BUILD_MAKEFILE
		else:
			install_dir_name = constants.INSTALL_DIR_GENERIC	
			makefile_name = constants.GENERIC_MAKEFILE		
				
		''' Target install del proyecto. Copia los archivos a SYSTEM '''
		do_make(paths.work_path + '/' + makefile_name, project_name + '_install')
		
		''' Si vamos a crear las imagenes el proyecto principal es rootfs. Creamos la imagen correspondiente (tftp o full)'''	
		if args.images:
			if build_type == constants.BUILD_TYPE_FULL:
				install_target_suffix = '-full'
			elif build_type == constants.BUILD_TYPE_TFTP:
				install_target_suffix = '-tftp'
			do_make(paths.work_path + '/' + makefile_name, project_name + '_install' + install_target_suffix)
				
			ret = os.system('sqlite3 ' + install_dir_name + '/home/sabt/data/db/system_db.db3 "update fw_info set fw_version=\'' + args.final_release_version + '\';"')
			if ret != 0:
				print_error("Error setting db fw info")
				raise Exception()
				
					
''' Crea el archivo .img con la imagen bruta '''
''' Utiliza makefile segun lo que se indica en el makefile del proyecto rootfs '''
def create_raw_image_file(project_tree, work_path, build_type, compiler):
	for version in project_tree[constants.ROOTFS_PROJECT]:
		project_name = utils.get_full_path(constants.ROOTFS_PROJECT, version, compiler)
		break
	
	if build_type == constants.BUILD_TYPE_TFTP:
		makefile_name = constants.TFTP_BUILD_MAKEFILE
	elif build_type == constants.BUILD_TYPE_FULL:
		makefile_name = constants.FULL_BUILD_MAKEFILE

	do_make(work_path + '/' + makefile_name, project_name + '_image')
		
		
''' Crea el archivo .bin con la imagen bruta mas el CRC '''
''' No ejecuta nada relacionado con los makefiles '''
def create_bin_image_file(part_number, dest_file, work_path):
	work_dir = work_path + "/bin_img_temp"
	raw_img_file = part_number + ".img"
	orig_raw_img_file_path = constants.ROOTFS_DIR + "/" + raw_img_file
	crc_file_path = work_dir + "/crc"
	tftp_img_file_path = dest_file
	
	os.system("rm -Rf " + work_dir)
	os.system("mkdir -p " + work_dir)
	if os.system("crc32 " + orig_raw_img_file_path + " | xxd -p -r > " + crc_file_path) != 0:
		print "Error creating crc file"
		raise Exception("Error generating CRC")
		
	f_crc = open(crc_file_path, "rb")
	f_raw_img = open(orig_raw_img_file_path, "rb")
	f_tftp_img = open(tftp_img_file_path, "wb")
	
	# Datos de la imagen
	byte = f_raw_img.read(1)
	while byte != "":
		f_tftp_img.write(byte)
		byte = f_raw_img.read(1)
	
	# CRC (4 bytes)
	byte = f_crc.read(1)
	while byte != "":
		f_tftp_img.write(byte)
		byte = f_crc.read(1)
		
	f_crc.close()
	f_raw_img.close()
	f_tftp_img.close()
	
	os.system("rm -Rf " + work_dir)
