import defines as constants

INCLUDE_PROJECTS_INCR = {}

def set_include_projects(version):
	global INCLUDE_PROJECTS_INCR
	if constants.GLOBAL_PROJECT == "UFD":
		if version == '1.2.5':
			INCLUDE_PROJECTS_INCR = {
				'402_00_libafs_cpp': 'YES',
				'402_00_improxy_cpp': 'YES',
				'402_00_cmm_cpp': 'YES',
				'402_00_login_reg_cpp': 'YES',
				'402_00_login_host_cpp': 'YES',
				'402_00_web_cpp': 'YES',
				'402_00_shell_cpp': 'YES',
				'402_00_qos_cpp': 'YES',
				'402_00_qos_fwupdate_cpp': 'YES',
				'402_00_restore_web_cpp': 'YES',
				'402_00_tasker_cpp': 'YES',
				'linux-kernel': 'YES',
				'rootfs': 'YES', 
			
				'boost' : 'YES',
				'busybox' : 'YES',
				'cppcms' : 'YES',
				'cracklib' : 'YES',
				'cryptodev' : 'YES',
				'curl' : 'YES',
				'e2fsprogs' : 'YES',
				'iptables' : 'YES',
				'libarchive' : 'YES',
				'libpcap' : 'YES',
				'linux-pam' : 'YES',
				'linux-kernel' : 'YES',
				'ncurses' : 'YES',
				'nginx' : 'YES',
				'nss-pam-ldapd' : 'YES',
				'openldap' : 'YES',
				'openssh' : 'YES',
				'openssl' : 'YES',
				'pcre' : 'YES',
				'pugixml' : 'YES',
				'rng-tools' : 'YES',
				'sqlite' : 'YES',

			}
	elif constants.GLOBAL_PROJECT == "IBD":
		if version == '1.2.5':
			INCLUDE_PROJECTS_INCR = {
				'402_00_libafs_cpp': 'YES',
				'402_00_improxy_cpp': 'YES',
				'402_00_cmm_cpp': 'YES',
				'402_00_login_reg_cpp': 'YES',
				'402_00_login_host_cpp': 'YES',
				'402_00_web_cpp': 'YES',
				'402_00_shell_cpp': 'YES',
				'402_00_qos_cpp': 'YES',
				'402_00_qos_fwupdate_cpp': 'YES',
				'402_00_restore_web_cpp': 'YES',
				'402_00_tasker_cpp': 'YES',
				'linux-kernel': 'YES',
				'rootfs': 'YES', 
			
				'boost' : 'YES',
				'busybox' : 'YES',
				'cppcms' : 'YES',
				'cracklib' : 'YES',
				'cryptodev' : 'YES',
				'curl' : 'YES',
				'e2fsprogs' : 'YES',
				'iptables' : 'YES',
				'libarchive' : 'YES',
				'libpcap' : 'YES',
				'linux-pam' : 'YES',
				'linux-kernel' : 'YES',
				'ncurses' : 'YES',
				'nginx' : 'YES',
				'nss-pam-ldapd' : 'YES',
				'openldap' : 'YES',
				'openssh' : 'YES',
				'openssl' : 'YES',
				'pcre' : 'YES',
				'pugixml' : 'YES',
				'rng-tools' : 'YES',
				'sqlite' : 'YES',
				'sqlitecpp' : 'YES',
				'tcpdump' : 'YES',
				'zeromq' : 'YES',
				'zlib' : 'YES',
				
				'u-boot' : 'YES',
			}
		elif version != "local":
			return 1
	
	return 0


