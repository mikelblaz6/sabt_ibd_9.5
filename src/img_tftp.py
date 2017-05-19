import subprocess, sys, os, shutil, zlib, time

import local
import utils
import defines as constants
import makeexe

HOME=os.getenv("HOME")


def create_file(part_number, dest_file, work_path):
	work_dir = work_path + "/tftp_temp"
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
	
	byte = f_crc.read(1)
	while byte != "":
		f_tftp_img.write(byte)
		byte = f_crc.read(1)
		
	byte = f_raw_img.read(1)
	while byte != "":
		f_tftp_img.write(byte)
		byte = f_raw_img.read(1)
	
	f_crc.close()
	f_raw_img.close()
	f_tftp_img.close()
	
	os.system("rm -Rf " + work_dir)
    

def create_tftp_img(args, work_path, fw_version = "local"):
	releases_dir = HOME + "/RELEASES/" + args.part_number + "/" + fw_version + "/TFTP/"
	os.system("mkdir -p " + releases_dir)
	dest_file = releases_dir + args.part_number + ".bin"
	
	makeexe.create_image(args, work_path)
	
	create_file(args.part_number, dest_file, work_path)

