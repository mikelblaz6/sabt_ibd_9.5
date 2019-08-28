import defines as constants

PROCESS_COMMITS = False
PROJECT_COMMITS = {}

def set_project_commits():
	global PROCESS_COMMITS
	global PROJECT_COMMITS
	
	if constants.GLOBAL_PROJECT == "402.12.00":
		PROCESS_COMMITS = True
		PROJECT_COMMITS = {
			'400_libutils_cpp': '705e189',
			'402_00_cmm_cpp': '8d4a4da',
			'402_00_improxy_cpp': '8cab761',
			'402_00_indust_cpp': 'e219736',
			'402_00_libafs_cpp': 'e743fe2e',	
			'402_00_libdlms_client_cpp': 'ab98de62',
			'402_00_login_host_cpp': '4e7b7cd',
			'402_00_login_reg_cpp': 'b201b86',
			'402_00_qos_cpp': '1954d2e',
			'402_00_qos_fwupdate_cpp': '73519bb',
			'402_00_restore_web_cpp': 'd70d9d1',
			'402_00_shell_cpp': 'cd67607',
			'402_00_tasker_cpp': '82bac96',
			'402_00_web_cpp': '08dd77f',
			'402_12_libam335x_cpp': '108a0ab',
			'402_12_libglcd_cpp': '10ccfc4',	
			'asio': '14561b1',
			'boost': '04bcdce',
			'busybox': '9793917',
			'cppcms': '40c30e5',
			'cracklib': '067a4f4',
			'cryptodev': '014d871',
			'curl': '1eff64e',
			'e2fsprogs': '7f9ca1a',
			'gsoap': '82a4685',
			'libarchive': '51cccb5',
			'libpcap': 'c564444',
			'linux-4.4.19': 'af29985',
			'linux-pam': '71d86f2',
			'ncurses': 'c776032',
			'nginx': 'bcf028b',
			'nss-pam-ldapd': 'f8fd09b',
			'openldap': 'fdd4310',
			'openssh': '505fe35',
			'openssl': '4290528',
			'pcre': 'b83cee6',
			'pugixml': '9eae795',
			'rng-tools': '5fe508a',
			'rootfs': '6aa0286',
			'sqlite': '7e5206c',
			'sqlitecpp': '5972b03',
			'tcpdump': 'f8f8189',
			'u-boot': '350ab95',
			'zeromq': '1e1ed2d',
			'zlib': '2bf9e47',
			 }
	elif constants.GLOBAL_PROJECT == "402.12.01":
		pass
	elif constants.GLOBAL_PROJECT == "402.12.02":
		pass
	elif constants.GLOBAL_PROJECT == "402.12.03":
		pass
	elif constants.GLOBAL_PROJECT == "402.12.04":
		pass
	elif constants.GLOBAL_PROJECT == "402.12.05.01":
		pass
	elif constants.GLOBAL_PROJECT == "402.12.06":
		pass
	elif constants.GLOBAL_PROJECT == "402.12.07":
		PROCESS_COMMITS = True
		PROJECT_COMMITS = {
			'400_libutils_cpp': '705e189',
			'402_00_cmm_cpp': '8d4a4da',
			'402_00_improxy_cpp': '8cab761',
			'402_00_indust_cpp': 'e219736',
			'402_00_libafs_cpp': '78383df9',	
			'402_00_libdlms_client_cpp': '45ea5b0f',
			'402_00_login_host_cpp': '4e7b7cd',
			'402_00_login_reg_cpp': 'b201b86',
			'402_00_qos_cpp': '1954d2e',
			'402_00_qos_fwupdate_cpp': 'dfa422f',
			'402_00_restore_web_cpp': 'd70d9d1',
			'402_00_shell_cpp': 'cd67607',
			'402_00_tasker_cpp': '82bac96',
			'402_00_web_cpp': '08dd77f',
			'402_12_libam335x_cpp': '8f7380a',
			'402_12_libglcd_cpp': '10ccfc4',	
			'asio': '14561b1',
			'boost': '04bcdce',
			'busybox': '9793917',
			'cppcms': '40c30e5',
			'cracklib': '067a4f4',
			'cryptodev': '014d871',
			'curl': '1eff64e',
			'e2fsprogs': '7f9ca1a',
			'gsoap': '82a4685',
			'libarchive': '51cccb5',
			'libpcap': 'c564444',
			'linux-4.4.19': 'af29985',
			'linux-pam': '71d86f2',
			'ncurses': 'c776032',
			'nginx': 'bcf028b',
			'nss-pam-ldapd': 'f8fd09b',
			'openldap': 'fdd4310',
			'openssh': '505fe35',
			'openssl': '4290528',
			'pcre': 'b83cee6',
			'pugixml': '9eae795',
			'rng-tools': '5fe508a',
			'rootfs': '73b453c',
			'sqlite': '7e5206c',
			'sqlitecpp': '5972b03',
			'tcpdump': 'f8f8189',
			'u-boot': 'cfe8d862',
			'zeromq': '1e1ed2d',
			'zlib': '2bf9e47',
			 }
