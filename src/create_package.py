#! /usr/bin/python
import os, logging, time, sys
import mrt_argparse
import defines as constants
import database


def pack_fw(dest_file, work_tmp_dir, files):
	compress_dir = work_tmp_dir + "/compress/"
	if os.system("mkdir -p " + compress_dir) != 0:
		print("Error packing fw incr")
		raise Exception()
	for lfile in files:
		if os.system("mv " + work_tmp_dir + "/"+ lfile + " " + compress_dir):
			print("Error moving file " + lfile + " to package")
			raise Exception()
	if os.system("tar -Jcf " + dest_file + " -C " + compress_dir + " " + " ".join([x for x in files])):
		print("Error incr image compressing")
		raise Exception()


def get_incr_update_files(args, work_dir, part_numbers, included_versions):
	sources_folder = constants.MRT_SERVER_FOLDER
	
	files = ["files.list"]
	for version in included_versions:
		files.append(constants.PRODUCT + "_" + version[0] + "_" + version[1] + "_incr.bin")
		os.system("cp " + sources_folder + "/FW_FAMILY/" + version[0] + "/" + version[1] + "/INCR/" + constants.PRODUCT + "_" + version[0] + "_" + version[1] + "_incr.bin " + work_dir)
	
	files_list_file = work_dir + "/files.list"
	fid = open(files_list_file, 'w')
	for pn in part_numbers:
		fid.write(pn[0] + "," + constants.PRODUCT + "_" + pn[1][0] + "_" + pn[1][1] + "_incr.bin\n")
	fid.close()
	
	return files
	
def get_full_update_files(args, work_dir, part_numbers, included_versions):
	sources_folder = constants.MRT_SERVER_FOLDER
	
	files = ["files.list"]
	for version in included_versions:
		files.append(constants.PRODUCT + "_" + version[0] + "_" + version[1] + "_full.bin")
		os.system("cp " + sources_folder + "/FW_FAMILY/" + version[0] + "/" + version[1] + "/FULL/" + constants.PRODUCT + "_" + version[0] + "_" + version[1] + "_full.bin " + work_dir)
	
	files_list_file = work_dir + "/files.list"
	fid = open(files_list_file, 'w')
	for pn in part_numbers:
		fid.write(pn[0] + "," + constants.PRODUCT + "_" + pn[1][0] + "_" + pn[1][1] + "_full.bin\n")
	fid.close()
	
	return files
	
		
def get_part_number_info(args, work_dir, included_versions, sql):
	
	part_numbers = []
	
	for version in included_versions:
		pns = sql.get_pn_comps_from_fam_fw(version[0], version[1])
		if len(pns) == 0:
			print "Error. Fw versions not found"
			raise Exception()
		for pn in pns:
			part_numbers.append((sql.get_part_number_name(pn[2])[0], version))
	return part_numbers
	
	
def add_digest(compress_file, dest_file, work_path):					
	priv_key = constants.SRC_DIR[1] + "/402_00_cmm_cpp/" + constants.CMM_PRIV_KEY_FILE
	pub_key = constants.SRC_DIR[1] + "/402_00_cmm_cpp/" + constants.CMM_PUB_KEY_FILE
	sign_file = work_path + "/sign.bin"

	
	if os.system("openssl dgst -MD5 -sign " + priv_key + " -out " + sign_file + " " + compress_file) != 0:
		print("Error generating digest")
		raise Exception()
		
	if os.system("openssl dgst -MD5 -verify " + pub_key + " -signature " + sign_file + " " + compress_file) != 0:
		print("Error checking digest")
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
	
	os.system("rm " + sign_file)
	
	
def create_package(args, work_path):
	sql = database.Database()
	
	fw_version = args.final_release_version
	if args.rc != None:
		fw_version = fw_version + "_rc" + str(args.rc)
		
	included_versions_tmp = args.compatible_versions.split(';')
	included_versions = []
	for included_vers_tmp in included_versions_tmp:
		included_versions.append((included_vers_tmp.split(',')[0], included_vers_tmp.split(',')[1]))
	
	#Generacion de actualizacion incr para la familia de fw
	releases_dir = constants.RELEASES_DIR + "/FW_FAMILY/PACKAGES/" + args.name + "/" + fw_version + "/"
	os.system("mkdir -p " + releases_dir)
	work_dir = work_path + "/package_temp/"
	os.system("rm -Rf " + work_dir)
	os.system("mkdir -p " + work_dir)
	
	if sql.VerifyNewPackage(args.compatible_versions) != 0:
		print "Error verifying included versions"
		exit(1)
	
	part_numbers = get_part_number_info(args, work_dir, included_versions, sql)
	
	#Incremental upd package
	dest_compress_file = work_dir + "/" + constants.PRODUCT + "_" + args.name + "_" + fw_version + "_package_incr.tar.xz"
	dest_file = releases_dir + constants.PRODUCT + "_" + args.name + "_" + fw_version + "_package_incr.bin"
	files = get_incr_update_files(args, work_dir, part_numbers, included_versions)
	pack_fw(dest_compress_file, work_dir, files)
	add_digest(dest_compress_file, dest_file, work_dir)
	
	#Full upd package
	os.system("rm -Rf " + work_dir)
	os.system("mkdir -p " + work_dir)
	dest_compress_file = work_dir + "/" + constants.PRODUCT + "_" + args.name + "_" + fw_version + "_package_full.tar.xz"
	dest_file = releases_dir + constants.PRODUCT + "_" + args.name + "_" + fw_version + "_package_full.bin"
	files = get_full_update_files(args, work_dir, part_numbers, included_versions)
	pack_fw(dest_compress_file, work_dir, files)
	add_digest(dest_compress_file, dest_file, work_dir)
	
	if args.final_release:
		sql.NewPackage(args.name, args.final_release_version, args.compatible_versions)
		sql.commit()


if __name__ == '__main__':
	parser = mrt_argparse.ArgumentParser(description='Create 402.12 firmware package with multiple fws')
	parser.add_argument('-c', '--compatible-versions', help='versions to include. Format: [FW_FAMILY,MIN_VERSION;]', required=True)
	parser.add_argument('-F', '--final-release', action='store_true', help='create final release storing version info in database')
	parser.add_argument('-V', '--final-release-version', help='set fw version for current release. Needed if --final-release active', required=True)
	parser.add_argument('-n', '--name', help='descriptive name', required=True)
	parser.add_argument('--rc', help='Set number for Release candidate versions', default=None)
	parsed_args = parser.parse_args()
	
	if parsed_args.rc != None and parsed_args.final_release == True:
		print "--rc option not compatible with --final-release"
		exit(1)
	
	prefix = "git" if parsed_args.final_release else "local"
	date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
	work_path = constants.MAIN_DIR + 'builds/'+ prefix+ '/package_' + parsed_args.name + '_' + parsed_args.final_release_version + '_' + date
	os.system('mkdir -p ' + work_path)
	
	create_package(parsed_args, work_path)
