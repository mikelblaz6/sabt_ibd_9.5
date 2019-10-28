#! /usr/bin/python
import os, logging, time, sys
import mrt_argparse
import defines as constants


''' Protege el archivo comprimido:
* Escribe los bytes MRT por delante para una comprobacion rapida en la web.
* A continuacion escribe el MD5 del comprimido a proteger
* A continuacion escribe el comprimido en si
'''
def add_digest(dest_file, private_key, public_key):
	sign_file = "sign.bin"
	
	if os.system("openssl dgst -MD5 -sign " + private_key + " -out " + sign_file + " " + dest_file + "_tmp") != 0:
		print_error("Error generating digest")
		raise Exception()
		
	if os.system("openssl dgst -MD5 -verify " + public_key + " -signature " + sign_file + " " + dest_file + "_tmp") != 0:
		print_error("Error checking digest")
		raise Exception()
		
	f_compress = open(dest_file + "_tmp", "rb")
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
	
	os.system("rm sign.bin")


def pack(pck_file, folder):
	os.system("tar -Jcf " + pck_file + "_tmp -C " + folder + " main.sh update_files")


if __name__ == '__main__':
	parser = mrt_argparse.ArgumentParser(description='Pack 402.12 firmware update packages')
	parser.add_argument('-f', '--file', help='destination file', required=True)
	parser.add_argument('-d', '--folder', help='folder to compress', required=True)
	parser.add_argument('-p', '--private-key', help='private key', required=True)
	parser.add_argument('-u', '--public-key', help='public key', required=True)
	args = parser.parse_args()
	
	pack(args.file, args.folder)
	
	add_digest(args.file, args.private_key, args.public_key)

	
'''Example:
python pack_update.py -d /home/jonathan/test -f /home/jonathan/MRT_incr_test.bin 
-p /home/jonathan/Dropbox/CodeBlocks/402_00_cmm_cpp/etc/cert_priv/fw_key.pem 
-u /home/jonathan/Dropbox/CodeBlocks/402_00_cmm_cpp/etc/cert/fw_key_pub.pem
'''
