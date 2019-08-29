import subprocess, sys, os, shutil, zlib, time
import img_tftp, makeexe

import local
import utils
import defines as constants
import database
import mrt_git

from utils import print_error
from include_projects import *

def prepare_incr_update_files(args, project_tree, paths, project_list, work_tmp_dir, compilation_id, sql):
	os.system("mkdir -p " + work_tmp_dir + "/update_files/system/")
	os.system("mkdir -p " + work_tmp_dir + "/update_files/files/")
	
	for version in project_tree[constants.ROOTFS_PROJECT]:
		project_name = utils.get_full_path(constants.ROOTFS_PROJECT, version)
		break
	for version in project_tree[constants.UBOOT_PROJECT]:
		uboot_project_name = utils.get_full_path(constants.UBOOT_PROJECT, version)
		break
				
	''' Rellenamos main.sh con la version de firmware a actualizar
	y la minima sobre la que se puede aplicar '''
	f = open(paths.build_path + "/" + project_name + constants.BUILD_TYPE_INCR_MAINSH_TEMPLATE, "r")
	text = f.read()
	f.close()
	tags = [("$FW_VERSION_PAR$", args.final_release_version), ("$MIN_VERSION_PAR$", args.previous_min_version),
			("$PART_NUMBER$", args.part_number)]
	
	f = open(work_tmp_dir + "/" + constants.MAINSH_FILE, "w")
	f.write(utils.replace_strings(text, tags))
	f.close()
	
	#print("Desea incluir el bootloader en la actualizacion incremental? (y/n)")
	#b = raw_input()
	if UPDATE_BOOTLOADER:
		project_list.append(constants.UBOOT_PROJECT)
		for temp_file in constants.UBOOT_FILES:
			if os.system("cp -af " + paths.deploy_path + "/" + uboot_project_name + "/" + temp_file + " " + work_tmp_dir + "/update_files/files/"):
				print_error("Error copying u-boot file", paths.deploy_path + "/" + uboot_project_name + "/" + temp_file)
				raise Exception()
		if args.final_release:
			for version in project_tree[constants.UBOOT_PROJECT]:
				break
			project_folder = utils.get_full_path(constants.UBOOT_PROJECT, version)
			project_build_path = paths.build_path + project_folder
			cur_version = mrt_git.get_last_tag(project_build_path)[1]
			sql.SetIncrUpdIncluded(compilation_id, constants.UBOOT_PROJECT, cur_version, incr_upd_included = 1)

	
	''' Rellenamos los scripts pre_actions.sh y post_actions.sh, y 
	copiamos los archivos necesarios a work_tmp_dir/update_files/files 
	'''
	pre_actions_text = ''
	post_action_text = ''
	for project in project_list:
		path = paths.build_path + "/" + project + constants.PROJECT_UPDATE_BASE + args.part_number + "/" + constants.PROJECT_UPDATE_PRE_CMDS_FILE
		text = ''
		try:
			with open(path, "r") as f:
				text = f.read()
		except:
			pass
		if text.strip() != '':
			pre_actions_text += text + "\n"

		path = paths.build_path + "/" + project + constants.PROJECT_UPDATE_BASE + constants.PROJECT_UPDATE_PRE_CMDS_FILE
		text = ''
		try:
			with open(path, "r") as f:
				text = f.read()
		except:
			pass
		if text.strip() != '':
			pre_actions_text += text + "\n"
		
		path = paths.build_path + "/" + project + constants.PROJECT_UPDATE_BASE + args.part_number + "/" + constants.PROJECT_UPDATE_POST_CMDS_FILE
		text = ''
		try:
			with open(path, "r") as f:
				text = f.read()
		except:
			pass
		if text.strip() != '':
			post_action_text += text + "\n"

		path = paths.build_path + "/" + project + constants.PROJECT_UPDATE_BASE + constants.PROJECT_UPDATE_POST_CMDS_FILE
		text = ''
		try:
			with open(path, "r") as f:
				text = f.read()
		except:
			pass
		if text.strip() != '':
			post_action_text += text + "\n"
		
		path = paths.build_path + "/" + project + constants.PROJECT_UPDATE_BASE + constants.PROJECT_UPDATE_EXTRA_FILES_FILE
		files = []
		try:
			with open(path, "r") as f:
				files = f.readlines()
		except:
			pass
		for cp_file in files:
			cp_file = cp_file.strip()
			if len(cp_file) != 0:
				if os.system("cp -af " + paths.build_path + "/" + project + constants.PROJECT_UPDATE_BASE + constants.PROJECT_UPDATE_EXTRA_FILES_PATH + cp_file + " " + work_tmp_dir + "/update_files/files/"):
					print_error("Error copying " + paths.build_path + "/" + project + constants.PROJECT_UPDATE_BASE + constants.PROJECT_UPDATE_EXTRA_FILES_PATH + cp_file)
					raise Exception()
				
	pre_actions_text += "exit 0;"	
	f = open(work_tmp_dir + "/update_files/pre_actions.sh", "w")
	f.write(pre_actions_text)
	f.close()
	
	''' Anadimos a post_actions la modificacion de la version de fw en la base de datos '''
	post_action_text += '/bin/sqlite3 /sabt/data/db/system_db.db3 "update fw_info set fw_ts = 0;"\n'
	post_action_text += '/bin/sqlite3 /sabt/data/db/system_db.db3 "update fw_info set fw_version=\'' + args.final_release_version + '\';" || exit 1\n'
	post_action_text += '/bin/sqlite3 /sabt/data/db/regs_db.db3 "update rtu_status set web_status=\'UPDATED\';" || exit 1\n'
	post_action_text += "exit 0;"
	f = open(work_tmp_dir + "/update_files/post_actions.sh", "w")
	f.write(post_action_text)
	f.close()
		
''' Mueve el contenido de SYSTEM_INCR a work_tmp_dir.
Mueve el contenido de work_tmp_dir al directorio de destino para comprimir.
Comprime en tar.xz '''
def pack_fw(dest_file, work_tmp_dir):
	if os.system("cp -aRf " + constants.INSTALL_DIR_INCR + "/* " + work_tmp_dir + "/update_files/system/"):
		print_error("Error copying incr image files")
		raise Exception()
	
	compress_dir = work_tmp_dir + "/compress/"
	if os.system("mkdir -p " + compress_dir) != 0:
		print_error("Error packing fw incr")
		raise Exception()
	if os.system("mv " + work_tmp_dir + "/main.sh " + compress_dir):
		print_error("Error moving main.sh file to package")
		raise Exception()
	if os.system("mv " + work_tmp_dir + "/update_files " + compress_dir):
		print_error("Error moving update_files folder to package")
		raise Exception()
	if os.system("tar -Jcf " + dest_file + " -C " + compress_dir + " main.sh update_files"):
		print_error("Error incr image compressing")
		raise Exception()
	
	
def create_incr_img(args, project_tree, project_list, paths, compilation_id, sql):
	releases_dir = os.getenv("HOME") + "/RELEASES/" + args.part_number + "/" + args.final_release_version + "/INCR/"
	os.system("mkdir -p " + releases_dir)
	work_dir = paths.work_path + "/incr_temp/"
	os.system("rm -Rf " + work_dir)
	os.system("mkdir -p " + work_dir)
	dest_compress_file = work_dir + "/MRT_" + args.part_number + "_" + args.final_release_version + "_incr.tar.xz"
	
	dest_file = releases_dir + "MRT_" + args.part_number + "_" + args.final_release_version + "_incr.bin"
	
	prepare_incr_update_files(args, project_tree, paths, project_list, work_dir, compilation_id, sql)
	
	pack_fw(dest_compress_file, work_dir)
	
	utils.add_digest(project_tree, dest_compress_file, dest_file, paths)
			
	os.system("rm -Rf " + work_dir)
