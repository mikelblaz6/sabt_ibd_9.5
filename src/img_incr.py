import subprocess, sys, os, shutil, zlib, time
import img_tftp, makeexe

import local
import utils
import defines as constants

HOME=os.getenv("HOME")

def set_full_upd_files(args, project_tree, project_list, work_path):
	os.system("mkdir -p " + work_path + "/update_files/system/")
	os.system("mkdir -p " + work_path + "/update_files/files/")
	
	cc_key = 'arm' if not args.no_cross_compile else 'x86'
	deb_key = 'debug' if args.debug else 'release'
	build_path = constants.build_paths[cc_key][deb_key]
	deploy_path = constants.deploy_paths[cc_key][deb_key]
	for project, project_data in project_tree.iteritems():
		if "rootfs" == project:
			for version, version_data in project_data.iteritems():
				project_name = utils.get_full_path(project, version)
		if "u-boot" == project:
			for version, version_data in project_data.iteritems():
				uboot_project_name = utils.get_full_path(project, version)
				
	ROOTFS_TEMPLATES_PATH = build_path + "/" + project_name + "/mrt/templates/incr_update/"
	temp_files = ("main.sh",)
	
	UBOOT_FILES_PATH = deploy_path + "/" + uboot_project_name
	
	pre_actions_text = ''
	post_action_text = ''
	
	print "Desea actualizar el bootloader en la actualizacion incremental? (y/n)"
	b = raw_input()
	if b=='y':
		project_list.append("u-boot")
		if os.system("cp -af " + UBOOT_FILES_PATH + "/MLO "  + work_path + "/update_files/files/"):
			raise Exception("Error copying u-boot files")
		if os.system("cp -af " + UBOOT_FILES_PATH + "/u-boot.img "  + work_path + "/update_files/files/"):
			raise Exception("Error copying u-boot files")
	
	for project in project_list:
		path = build_path + "/" + project + "/mrt/incr_update/pre_cmds.tmpl"
		text = ''
		try:
			with open(path, "r") as f:
				text = f.read()
		except:
			pass
		if text.strip() != '':
			pre_actions_text += text + "\n"
		
		path = build_path + "/" + project + "/mrt/incr_update/post_cmds.tmpl"
		text = ''
		try:
			with open(path, "r") as f:
				text = f.read()
		except:
			pass
		if text.strip() != '':
			post_action_text += text + "\n"
		
		path = build_path + "/" + project + "/mrt/incr_update/files"
		files = []
		try:
			with open(path, "r") as f:
				files = f.readlines()
		except:
			pass
		for cp_file in files:
			cp_file = cp_file.strip()
			if len(cp_file) != 0:
				os.system("cp -af " + build_path + "/" + project + "/mrt/incr_update/" + cp_file + " " + work_path + "/update_files/files/")
				
			
	for temp_file in temp_files:
		f = open(ROOTFS_TEMPLATES_PATH + temp_file, "r")
		text = f.read()
		f.close()
		tags = [("$FW_VERSION_PAR$", args.final_release_version),
				("$MIN_VERSION_PAR$", args.previous_min_version),]
		
		f = open(work_path + temp_file, "w")
		f.write(utils.replace_strings(text, tags))
		f.close()
		
	
		
	f = open(work_path + "/update_files/pre_actions.sh", "w")
	f.write(pre_actions_text)
	f.close()
	
	post_action_text += '/bin/sqlite3 /sabt/data/db/system_db.db3 "update fw_info set fw_version=\'' + args.final_release_version + '\';"\n'
	post_action_text += '/bin/sqlite3 /sabt/data/db/regs_db.db3 "update rtu_status set web_status=\'UPDATED\';"\n'
	f = open(work_path + "/update_files/post_actions.sh", "w")
	f.write(post_action_text)
	f.close()
	
	os.system("mkdir -p " + constants.INSTALL_DIR_INCR)
	p = subprocess.Popen(['make', '-f', work_path + '/../Makefile_incr', 'incr_release'], close_fds = True)
	p.communicate()
	if p.returncode != 0:
		raise Exception("Error creating incremental image")
	
	ret = os.system("cp -aRf " + constants.INSTALL_DIR_INCR + "/* " + work_path + "/update_files/system/")
	if ret != 0:
		raise Exception("Error copying update files")


def pack_fw(part_number, dest_file, work_path):
	compress_dir = work_path + "/compress/"
	if os.system("mkdir -p " + compress_dir) != 0:
		raise Exception("Error packing fw 1")
	if os.system("mv " + work_path + "/main.sh " + compress_dir):
		raise Exception("Error packing fw 1")
	if os.system("mv " + work_path + "/update_files " + compress_dir):
		raise Exception("Error packing fw 1")
	if os.system("tar -Jcf " + dest_file + " -C " + compress_dir + " main.sh update_files"):
		raise Exception("Error packing fw 1")
	
def add_digest(args, project_tree, compress_file, dest_file, work_path):
	cc_key = 'arm' if not args.no_cross_compile else 'x86'
	deb_key = 'debug' if args.debug else 'release'
	build_path = constants.build_paths[cc_key][deb_key]
	for project, project_data in project_tree.iteritems():
		if "402_00_cmm_cpp" == project:
			for version, version_data in project_data.iteritems():
				project_name = utils.get_full_path(project, version)
					
	
	priv_key = build_path + "/" + project_name + "/etc/cert_priv/fw_key.pem"
	pub_key = build_path + "/" + project_name + "/etc/cert/fw_key_pub.pem"
	sign_file = work_path + "/sign.bin"
	
	if os.system("openssl dgst -MD5 -sign " + priv_key + " -out " + sign_file + " " + compress_file) != 0:
		raise Exception("Error generating digest")
		
	if os.system("openssl dgst -MD5 -verify " + pub_key + " -signature " + sign_file + " " + compress_file) != 0:
		raise Exception("Error checking digest")
		
	f_compress = open(compress_file, "rb")
	f_sign = open(sign_file, "rb")
	f_dest_img = open(dest_file, "wb")
	
	#Anadimos MRT por delante
	f_dest_img.write('M')
	f_dest_img.write('R')
	f_dest_img.write('T')
	
	#Anadimos firma
	byte = f_sign.read(1)
	while byte != "":
		f_dest_img.write(byte)
		byte = f_sign.read(1)
		
	byte = f_compress.read(1)
	while byte != "":
		f_dest_img.write(byte)
		byte = f_compress.read(1)
	
	f_compress.close()
	f_sign.close()
	f_dest_img.close()


def create_web_img(args, project_tree, project_list, work_path):
	fw_version = args.final_release_version
	releases_dir = HOME + "/RELEASES/" + args.part_number + "/" + fw_version + "/INCR/"
	os.system("mkdir -p " + releases_dir)
	work_dir = work_path + "/incr_temp/"
	os.system("rm -Rf " + work_dir)
	os.system("mkdir -p " + work_dir)
	dest_compress_file = work_dir + "/MRT_" + args.part_number + "_" + fw_version + "_incr.tar.xz"
	
	dest_file = releases_dir + "MRT_" + args.part_number + "_" + fw_version + "_incr.bin"
	
	set_full_upd_files(args, project_tree, project_list, work_dir)
	
	pack_fw(args.part_number, dest_compress_file, work_dir)
	
	add_digest(args, project_tree, dest_compress_file, dest_file, work_dir)
			
	os.system("rm -Rf " + work_dir)
