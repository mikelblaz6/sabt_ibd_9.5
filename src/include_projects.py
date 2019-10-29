import defines as constants

INCLUDE_PROJECTS_INCR = {}
UPDATE_BOOTLOADER = False

def set_include_projects():
	global INCLUDE_PROJECTS_INCR
	global UPDATE_BOOTLOADER
	if constants.GLOBAL_PROJECT == "UFD":
		INCLUDE_PROJECTS_INCR = {
			'402_00_tasker_cpp': 'YES',
		}
	elif constants.GLOBAL_PROJECT == "IBD":
		INCLUDE_PROJECTS_INCR = {

		}
		UPDATE_BOOTLOADER = False


