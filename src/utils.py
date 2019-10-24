import defines as constants

import os,sys


def get_full_path(project, version, compiler):
	version_str = '' if version == None else ('_git')
	if compiler != "7": 
		version_str = version_str + '_cpp5'
	else:
		version_str = version_str + '_cpp7'

	return str(project) + version_str


def replace_strings(text, tags):
	for tag in tags:
		text = text.replace(tag[0], tag[1])
	return text


def print_error(text):
	print >> sys.stderr, text


''' Protege el archivo comprimido:
* Escribe los bytes MRT por delante para una comprobacion rapida en la web.
* A continuacion escribe el MD5 del comprimido a proteger
* A continuacion escribe el comprimido en si
'''
def add_digest(project_tree, compress_file, dest_file, paths, compiler):
	for version in project_tree[constants.CMM_PROJECT]:
		project_name = get_full_path(constants.CMM_PROJECT, version, compiler)
		break
					
	priv_key = paths.build_path + "/" + project_name + constants.CMM_PRIV_KEY_FILE
	pub_key = paths.build_path + "/" + project_name + constants.CMM_PUB_KEY_FILE
	sign_file = paths.work_path + "/sign.bin"
	
	if os.system("openssl dgst -MD5 -sign " + priv_key + " -out " + sign_file + " " + compress_file) != 0:
		print_error("Error generating digest")
		raise Exception()
		
	if os.system("openssl dgst -MD5 -verify " + pub_key + " -signature " + sign_file + " " + compress_file) != 0:
		print_error("Error checking digest")
		raise Exception()
		
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
	
	
def get_fw_tar(fw_file, dest_folder):
	tar_file = "compress.tar.xz"
	
	f_fw_file= open(fw_file, "rb")
	f_tar_file = open(dest_folder + "/" + tar_file, "wb")
	f_fw_file.read(3+256)
	byte = f_fw_file.read(1)
	while byte != "":
		f_tar_file.write(byte)
		byte = f_fw_file.read(1)
	f_fw_file.close()
	f_tar_file.close()


if __name__ == '__main__':
	get_fw_tar(sys.argv[1], sys.argv[2])



	
