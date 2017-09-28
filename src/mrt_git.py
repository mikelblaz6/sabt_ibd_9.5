#! /usr/bin/python
import subprocess, shutil, os, sys

import defines as constants
import utils

def clone(namespace, project, path):
	p = subprocess.Popen(['git', 'clone', 'git@gitlab.merytronic.com:' + namespace + '/' + project + '.git', path], close_fds = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	p.communicate()
	if p.returncode != 0:
		return 1
	return 0
	
	
def checkout(path, commit):
	p = subprocess.Popen(['git', '-C', path, 'checkout', commit], close_fds = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	p.communicate()
	if p.returncode != 0:
		return 1
	return 0
	
	
def get_last_tag(path):
	p = subprocess.Popen(['git', '-C', path, 'describe', '--abbrev=0', '--tags'], close_fds = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	(stdout, stderr) = p.communicate()
	if p.returncode != 0:
		return (1,"")
	return (0, stdout.strip())


def get_current_commit(path):
	p = subprocess.Popen(['git', '-C', path, 'log', '-1', '--pretty=format:%h'], close_fds = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	(stdout, stderr) = p.communicate()
	if p.returncode != 0:
		return (1,"")
	return (0, stdout.strip())


def get_project_source(project, build_path):
	print "Getting git sources for " + project
	tmp_build_path = build_path + '/' + project + '_tmp'
	if os.path.isdir(tmp_build_path):
		shutil.rmtree(tmp_build_path)
		
	for namespace in constants.GIT_NAMESPACES:
		if clone(namespace, project, tmp_build_path) == 0:
			break
	
	branch_name = ''
	for branch in constants.GIT_BRANCHES:
		if checkout(tmp_build_path, branch) == 0:
			print "Checkout on branch", branch,"for project",project
			branch_name = branch
			break
	if branch_name == '':
		raise Exception("Branch for project " + project + " not found in GIT")
			

	(ok, branch_version) = get_last_tag(tmp_build_path)
	if branch != 'master':
		version = branch_version[len(branch)+1:]  #Eg: 402/vX.Y.Z, solo interesa vX.Y.Z
	else:
		version = branch_version  #Eg: vX.Y.Z, solo interesa vX.Y.Z
	if version[0] == 'v':
		version = version[1:]   #Quitamos la 'v'

		
	if os.path.isdir(build_path + utils.get_full_path(project, version)):
		shutil.rmtree(build_path + utils.get_full_path(project, version))
	shutil.move(tmp_build_path, build_path + utils.get_full_path(project, version))
	
	return version
	
			

