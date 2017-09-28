import subprocess, sys, os, shutil, zlib, time

import local
import utils
import defines as constants
import makeexe

def create_tftp_img(project_tree, args, paths):
	releases_dir = os.getenv("HOME") + "/RELEASES/" + args.part_number + "/" + args.final_release_version + "/TFTP/"
	os.system("mkdir -p " + releases_dir)
	dest_file = releases_dir + args.part_number + ".bin"
	
	# makefile sobre target rootfs_image
	makeexe.create_raw_image_file(project_tree, paths.work_path, constants.BUILD_TYPE_TFTP)
	makeexe.create_bin_image_file(args.part_number, dest_file, paths.work_path)

