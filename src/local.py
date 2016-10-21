import ConfigParser, os, shutil
import defines as constants
import utils

def search_project_path(project):
	test_paths = []
	if isinstance(constants.SRC_DIR, list) or isinstance(constants.SRC_DIR, tuple):
		test_paths.extend(constants.SRC_DIR)
	else:
		test_paths.append(constants.SRC_DIR)
		
	found = False
	for path in test_paths:
		if os.path.isdir(path + project):
			found = True
			break
	if not found:
		raise Exception('Project ' + project + ' sources not found')
	return path


def prepare_local(project, version, build_path):
	source_path = search_project_path(project)
	project_build_path = build_path + utils.get_full_path(project, version)
	if os.path.isdir(project_build_path):
		shutil.rmtree(project_build_path)
		
	shutil.copytree(source_path + project, project_build_path, symlinks=True)
		
def prepare_deploy(project, version, deploy_path):
	project_deploy_path = deploy_path + utils.get_full_path(project, version)
	if os.path.isdir(project_deploy_path):
		shutil.rmtree(project_deploy_path)
