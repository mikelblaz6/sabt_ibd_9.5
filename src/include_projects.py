import defines as constants

INCLUDE_PROJECTS_INCR = {}

def set_include_projects(version):
	global INCLUDE_PROJECTS_INCR
	if constants.GLOBAL_PROJECT == "UFD":
		if version == '1.2.8' or version =='1.2.9' or version == '1.2.10':
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
				'ncurses' : 'YES',
				'nginx' : 'YES',
				'nss-pam-ldapd' : 'YES',
				'openldap' : 'YES',
				'openssh' : 'YES',
				'openssl' : 'YES',
				'pcre' : 'YES',
				'pugixml' : 'YES',
				'rng-tools' : 'YES',
				'sqldiff' : 'YES',
				'sqlite' : 'YES',
				'sqlitecpp' : 'YES',
				'tz' : 'YES',
				'tcpdump' : 'YES',
				'zeromq' : 'YES',
				'zlib' : 'YES',
				
				'u-boot' : 'YES',
			}
		elif version == '1.2.11':
			INCLUDE_PROJECTS_INCR = {
				'402_00_tasker_cpp': 'YES',
			}
		elif version == '1.2.12':
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
				'cppcms' : 'YES',
				'u-boot' : 'YES',
			}
		elif '9.9.' in version:
			return 0
		elif version != "local":
			return 1
	elif constants.GLOBAL_PROJECT == "IBD":
		if version == '1.2.5' or version == '1.2.6' or version == '1.2.7' or version == '1.2.8' or version =='1.2.9':
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
				'ncurses' : 'YES',
				'nginx' : 'YES',
				'nss-pam-ldapd' : 'YES',
				'openldap' : 'YES',
				'openssh' : 'YES',
				'openssl' : 'YES',
				'pcre' : 'YES',
				'pugixml' : 'YES',
				'rng-tools' : 'YES',
				'sqldiff' : 'YES',
				'sqlite' : 'YES',
				'sqlitecpp' : 'YES',
				'tz' : 'YES',
				'tcpdump' : 'YES',
				'zeromq' : 'YES',
				'zlib' : 'YES',
				
				'u-boot' : 'YES',
			}
		elif version == '1.2.10':
			INCLUDE_PROJECTS_INCR = {
				'402_00_libafs_cpp': 'YES',
				'402_00_improxy_cpp': 'YES',
				'402_00_cmm_cpp': 'YES',
				'402_00_login_reg_cpp': 'YES',
				'402_00_login_host_cpp': 'YES',
				'402_00_web_cpp': 'YES',
				'402_00_shell_cpp': 'YES',
				'402_00_qos_cpp': 'YES',
				'402_00_tasker_cpp': 'YES',
				
				'u-boot' : 'YES',
			}
		elif version == '1.2.12':
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
				'cppcms' : 'YES',
				'u-boot' : 'YES',
			}
		elif version == '1.3.1':
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
				'cppcms' : 'YES',
				'u-boot' : 'YES',
				'rootfs' : 'YES',
				'linux-kernel': 'YES',
			}
		elif '9.9.' in version:
			return 0
		elif version != "local":
			return 1
	elif constants.GLOBAL_PROJECT == "MRT":
		if version =='1.2.10':
			INCLUDE_PROJECTS_INCR = {
				'400_libmodbus_c': 'YES',
				'400_mcutils_c': 'YES',
				'402_00_libafs_cpp': 'YES',
				'402_00_improxy_cpp': 'YES',
				'402_00_cmm_cpp': 'YES',
				'402_00_login_reg_cpp': 'YES',
				'402_00_login_host_cpp': 'YES',
				'402_00_web_cpp': 'YES',
				'402_00_shell_cpp': 'YES',
				'402_00_qos_cpp': 'YES',
				'402_00_tasker_cpp': 'YES',
				'402_00_modbus_cpp': 'YES',
				
				'u-boot' : 'YES',
			}
		elif version == '1.2.12':
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
				'400_libmodbus_c': 'YES',
				'400_mcutils_c': 'YES',
				'402_00_modbus_cpp': 'YES',
				'cppcms' : 'YES',
				'u-boot' : 'YES',
			}
		elif '9.9.' in version:
			return 0
		elif version != "local":
			return 1
	elif constants.GLOBAL_PROJECT == "MLY":
		if version =='1.2.10':
			INCLUDE_PROJECTS_INCR = {
				'400_libmodbus_c': 'YES',
				'400_mcutils_c': 'YES',
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
				'402_00_lcd_keyb_cpp': 'YES',
				'402_00_modbus_cpp': 'YES',
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
				'ncurses' : 'YES',
				'nginx' : 'YES',
				'nss-pam-ldapd' : 'YES',
				'openldap' : 'YES',
				'openssh' : 'YES',
				'openssl' : 'YES',
				'pcre' : 'YES',
				'pugixml' : 'YES',
				'rng-tools' : 'YES',
				'sqldiff' : 'YES',
				'sqlite' : 'YES',
				'sqlitecpp' : 'YES',
				'tz' : 'YES',
				'tcpdump' : 'YES',
				'zeromq' : 'YES',
				'zlib' : 'YES',
				
				'u-boot' : 'YES',
			}
		elif version == '1.2.12':
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
				'400_libmodbus_c': 'YES',
				'400_mcutils_c': 'YES',
				'402_00_modbus_cpp': 'YES',
				'cppcms' : 'YES',
				'u-boot' : 'YES',
				'402_00_lcd_keyb_cpp': 'YES',
			}
		elif '9.9.' in version:
			return 0
		elif version != "local":
			return 1
	return 0


