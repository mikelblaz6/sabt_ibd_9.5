import subprocess, sys, os, shutil, zlib, time

import local
import utils
import defines as constants
import makeexe

def create_tftp_img(project_tree, args, paths):
	fw_version = utils.get_rc_fw_version(args)
		
	releases_dir = os.getenv("HOME") + "/RELEASES/FW_FAMILY/" + args.fw_family + "/" + fw_version + "/TFTP/"
	os.system("mkdir -p " + releases_dir)
	dest_file = releases_dir + constants.PRODUCT + ".bin"
	
	# makefile sobre target rootfs_image
	makeexe.create_raw_image_file(project_tree, paths.work_path, constants.BUILD_TYPE_TFTP, args.compiler)
	makeexe.create_bin_image_file(dest_file, paths.work_path)
	
	for pn in args.part_number_list.split(","):
		releases_dir = os.getenv("HOME") + "/RELEASES/" + pn + "/" + fw_version + "/TFTP/"
		os.system("rm -Rf " + releases_dir)
		os.system("mkdir -p " + releases_dir)
		pn_specific_dest_file = releases_dir  + pn + ".bin"
		os.system("cp " + dest_file + " " + pn_specific_dest_file)

