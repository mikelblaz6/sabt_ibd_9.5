import subprocess, sys, os, shutil, zlib, time
import makeexe

import local
import utils
import defines as constants
import database
import mrt_git

from utils import print_error
from include_projects import *

uboot_included = False

#TODO: FALTARIA INCLUIR ARCHIVO COMMANDS.TXT PARA EL BOOTLOADER?????

''' Rellenamos main.sh con los datos de version de firmware 
Si se solicita incluimos archivos del bootloader 
Dejamos en work_tmp_dir los archivos:
	* 402.12.xx.bin
	* main.sh
	* Opcional: MLO
	* Opcional: u-boot.img
'''
def prepare_full_update_files(args, project_tree, paths, work_tmp_dir, compilation_id, sql):
	global uboot_included

	for version in project_tree[constants.ROOTFS_PROJECT]:
		project_name = utils.get_full_path(constants.ROOTFS_PROJECT, version)
		break
	for version in project_tree[constants.UBOOT_PROJECT]:
		uboot_project_name = utils.get_full_path(constants.UBOOT_PROJECT, version)
		break
				
	''' Rellenamos main.sh con la version de firmware '''
	f = open(paths.build_path + "/" + project_name + constants.BUILD_TYPE_FULL_MAINSH_TEMPLATE, "r")
	text = f.read()
	f.close()
	tags = [("$FW_VERSION_PAR$", args.final_release_version)]
	
	f = open(work_tmp_dir + "/" + constants.MAINSH_FILE, "w")
	f.write(utils.replace_strings(text, tags))
	f.close()
	
	for project in project_tree:
		include_in_database = True
		if project == constants.UBOOT_PROJECT:
			#print("Desea incluir el bootloader en la actualizacion completa (full)? (y/n)")
			#b = raw_input()
			if UPDATE_BOOTLOADER:
				uboot_included = True
				for temp_file in constants.UBOOT_FILES:
					if os.system("cp -af " + paths.deploy_path + "/" + uboot_project_name + "/" + temp_file + " " + work_tmp_dir):
						print_error("Error copying u-boot file", paths.deploy_path + "/" + uboot_project_name + "/" + temp_file)
						raise Exception()
			else:
				include_in_database = False
				
		if args.final_release and include_in_database:
			for tree_version in project_tree[project]:
				break
			project_folder = utils.get_full_path(project, tree_version)
			project_build_path = paths.build_path + project_folder
			cur_version = mrt_git.get_last_tag(project_build_path)[1]
			sql.SetFullUpdIncluded(compilation_id, project, cur_version, full_upd_included = 1)

''' Mueve el contenido de work_tmp_dir al directorio de destino para comprimir.
Comprime en tar.xz '''
def pack_fw(part_number, dest_file, work_tmp_dir):
	global uboot_included
	tftp_img_file = part_number + ".bin"
	compress_dir = work_tmp_dir + "/compress/"
	if os.system("mkdir -p " + compress_dir):
		print_error("Error packing fw full")
		raise Exception()
	if os.system("mv " + work_tmp_dir + "/main.sh " + compress_dir):
		print_error("Error moving main.sh file to package")
		raise Exception()
	if uboot_included:
		if os.system("mv " + work_tmp_dir + "/MLO " + compress_dir):
			print_error("Error packing fw MLO")
			raise Exception()
		if os.system("mv " + work_tmp_dir + "/u-boot.img " + compress_dir):
			print_error("Error packing fw u-boot")
			raise Exception()
	if os.system("mv " + work_tmp_dir + "/" + tftp_img_file + " " + compress_dir):
		print_error("Error packing fw cannot move image")
		raise Exception()
	if uboot_included:
		files_to_compress = " " + constants.MAINSH_FILE + " " + constants.UBOOT_FILES[0] + " " +  constants.UBOOT_FILES[1] + " " + tftp_img_file
	else:
		files_to_compress = " " + constants.MAINSH_FILE + " " + tftp_img_file
	if os.system("tar -Jcf " + dest_file + " -C " + compress_dir + files_to_compress):
		print_error("Error full image compressing")
		raise Exception()
	
	



def create_full_img(args, project_tree, paths, compilation_id, sql):
	fw_version = args.final_release_version
	releases_dir = os.getenv("HOME") + "/RELEASES/" + args.part_number + "/" + fw_version + "/FULL/"
	os.system("mkdir -p " + releases_dir)
	work_dir = paths.work_path + "/full_temp/"
	os.system("rm -Rf " + work_dir)
	os.system("mkdir -p " + work_dir)
	dest_tftp_img_file = work_dir + "/" + args.part_number + ".bin"
	dest_compress_file = work_dir + "/MRT_" + args.part_number + "_" + fw_version + "_full.tar.xz"
	
	dest_file = releases_dir + "MRT_" + args.part_number + "_" + fw_version + "_full.bin"
	
	# Realiza los cambios necesarios sobre el sistema ya compilado e instalado en SYSTEM
	prepare_full_update_files(args, project_tree, paths, work_dir, compilation_id, sql)
	
	makeexe.create_raw_image_file(project_tree, paths.work_path, constants.BUILD_TYPE_FULL)
	makeexe.create_bin_image_file(args.part_number, dest_tftp_img_file, work_dir)
	
	pack_fw(args.part_number, dest_compress_file, work_dir)
	
	utils.add_digest(project_tree, dest_compress_file, dest_file, paths)
			
	os.system("rm -Rf " + work_dir)
