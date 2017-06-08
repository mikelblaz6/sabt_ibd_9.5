import subprocess, sys, os, shutil, zlib, time
import img_tftp, makeexe

import local
import utils
import defines as constants

HOME=os.getenv("HOME")

uboot_included = False

# Rellenamos las templates con los datos de version de firmware
# Nos aseguramos de borrar scripts de inicio que no se usaran (check_eeprom)
def set_full_upd_files(args, project_tree, work_path):
	global uboot_included
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
				
	ROOTFS_TEMPLATES_PATH = build_path + "/" + project_name + "/mrt/templates/full_update/"
	temp_files = ["main.sh",]
	boot_files = []
	
	UBOOT_FILES_PATH = deploy_path + "/" + uboot_project_name
	
	print "Desea actualizar el bootloader en la actualizacion completa? (y/n)"
	b = raw_input()
	if b=='y':
		uboot_included = True
		boot_files.append(UBOOT_FILES_PATH + "/MLO")
		boot_files.append(UBOOT_FILES_PATH + "/u-boot.img")
	
	for temp_file in temp_files:
		f = open(ROOTFS_TEMPLATES_PATH + temp_file, "r")
		text = f.read()
		f.close()
		tags = [("$FW_VERSION_PAR$", args.final_release_version)]
		
		f = open(work_path + temp_file, "w")
		f.write(utils.replace_strings(text, tags))
		f.close()
		
	for temp_file in boot_files:
		if os.system("cp -af " + temp_file + " " + work_path):
			raise Exception("Error copying u-boot files")

def pack_fw(part_number, dest_file, work_path):
	global uboot_included
	tftp_img_file = part_number + ".bin"
	compress_dir = work_path + "/compress/"
	if os.system("mkdir -p " + compress_dir) != 0:
		raise Exception("Error packing fw 1")
	if os.system("mv " + work_path + "/main.sh " + compress_dir):
		raise Exception("Error packing fw 1")
	if uboot_included:
		if os.system("mv " + work_path + "/MLO " + compress_dir):
			raise Exception("Error packing fw uboot")
		if os.system("mv " + work_path + "/u-boot.img " + compress_dir):
			raise Exception("Error packing fw uboot")
	if os.system("mv " + work_path + "/" + tftp_img_file + " " + compress_dir):
		raise Exception("Error packing fw 1")
	if uboot_included:
		files_to_compress = " main.sh MLO u-boot.img " + tftp_img_file
	else:
		files_to_compress = " main.sh " + tftp_img_file
	if os.system("tar -Jcf " + dest_file + " -C " + compress_dir + files_to_compress):
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


def create_web_img(args, project_tree, work_path):
	fw_version = args.final_release_version
	releases_dir = HOME + "/RELEASES/" + args.part_number + "/" + fw_version + "/FULL/"
	os.system("mkdir -p " + releases_dir)
	work_dir = work_path + "/web_temp/"
	os.system("rm -Rf " + work_dir)
	os.system("mkdir -p " + work_dir)
	dest_tftp_img_file = work_dir + "/" + args.part_number + ".bin"
	dest_compress_file = work_dir + "/MRT_" + args.part_number + "_" + fw_version + "_full.tar.xz"
	
	dest_file = releases_dir + "MRT_" + args.part_number + "_" + fw_version + "_full.bin"
	
	set_full_upd_files(args, project_tree, work_dir)
	makeexe.create_image(args, work_path, "full")

	img_tftp.create_file(args.part_number, dest_tftp_img_file, work_dir)
	
	pack_fw(args.part_number, dest_compress_file, work_dir)
	
	add_digest(args, project_tree, dest_compress_file, dest_file, work_dir)
			
	os.system("rm -Rf " + work_dir)
