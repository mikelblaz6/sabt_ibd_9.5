#! /usr/bin/python
import os, logging, time, sys
import mrt_argparse
import defines as constants



def extract(pck_file, folder):
	tar_fid = open(folder + "/upd.tar.xz", "wb")
	fid = open(pck_file, "rb")
	fid.seek(3+256)
	byte = fid.read(1)
	while byte != "":
		tar_fid.write(byte)
		byte = fid.read(1)
	tar_fid.close()
	fid.close()
	
	os.system("tar -xf " + folder +  "/upd.tar.xz -C " + folder + "/")
	os.system("rm -f " + folder +  "/upd.tar.xz")



if __name__ == '__main__':
	parser = mrt_argparse.ArgumentParser(description='Extract 402.12 firmware update packages')
	parser.add_argument('-f', '--file', help='file to extract', required=True)
	parser.add_argument('-d', '--folder', help='destiny folder', default = ".")
	args = parser.parse_args()
	
	
	os.system("mkdir -p " + args.folder)

	extract(args.file, args.folder)

	
'''Example:
python extract_update.py -f /home/jonathan/MRT_402.12.00_1.1.0_incr.bin -d /home/jonathan/test
'''
