import defines as constants

INCLUDE_PROJECTS_INCR = {}
UPDATE_BOOTLOADER = False

def set_include_projects():
	global INCLUDE_PROJECTS_INCR
	global UPDATE_BOOTLOADER
	if constants.GLOBAL_PROJECT == "402.12.00":
		INCLUDE_PROJECTS_INCR = {
			'402_00_libafs_cpp': 'YES',
			'402_00_tasker_cpp': 'YES',
		}
	elif constants.GLOBAL_PROJECT == "402.12.01":
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
			'tz' : 'YES',
			'u-boot' : 'YES',
			'zeromq' : 'YES',
			'zlib' : 'YES',
		}

		UPDATE_BOOTLOADER = True
	elif constants.GLOBAL_PROJECT == "402.12.02":
		
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
			'linux-4.4.19': 'YES',
			'rootfs': 'YES', }

		UPDATE_BOOTLOADER = True
	elif constants.GLOBAL_PROJECT == "402.12.03":
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
			'u-boot' : 'YES',
			'zeromq' : 'YES',
			'zlib' : 'YES',
		}

		UPDATE_BOOTLOADER = True
	elif constants.GLOBAL_PROJECT == "402.12.04":
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

			'tz' : 'YES',
			'rootfs' : 'YES',
		}

	elif constants.GLOBAL_PROJECT == "402.12.05.01":
		INCLUDE_PROJECTS_INCR = {
			'402_00_cmm_cpp': 'YES',
			'402_00_libafs_cpp': 'YES',
			'402_00_qos_cpp': 'YES',
			'402_00_tasker_cpp': 'YES',
			'402_00_web_cpp': 'YES',
			'402_00_improxy_cpp': 'YES',
			'402_00_login_reg_cpp': 'YES',
			'402_00_login_host_cpp': 'YES',
			'402_00_shell_cpp': 'YES',
			'402_00_lcd_keyb_cpp': 'YES',
			'402_00_restore_web_cpp': 'YES',
			'rootfs': 'YES',
		}

		UPDATE_BOOTLOADER = True
	elif constants.GLOBAL_PROJECT == "402.12.06":
		pass
	elif constants.GLOBAL_PROJECT == "402.12.07":
		INCLUDE_PROJECTS_INCR = {
			'402_00_libafs_cpp': 'YES',
			'402_00_tasker_cpp': 'YES',
		}

