#! /usr/bin/python
import subprocess, shutil, os, sys

import defines as constants
import utils
import project_commits as pr_comm

def clone(namespace, project, path):
	p = subprocess.Popen(['git', 'clone', constants.GIT_URL + '/' + namespace + '/' + project + '.git', path], close_fds = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
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


def get_project_source(project, build_path, compiler):
	print "Getting git sources for " + project
	tmp_build_path = build_path + '/' + project + '_tmp'
	if os.path.isdir(tmp_build_path):
		shutil.rmtree(tmp_build_path)
		
	for namespace in constants.GIT_NAMESPACES:
		if clone(namespace, project, tmp_build_path) == 0:
			break
	
	branch_name = ''
	if pr_comm.PROCESS_COMMITS == True and project in pr_comm.PROJECT_COMMITS:
		if checkout(tmp_build_path, pr_comm.PROJECT_COMMITS[project]) == 0:
			print "Checkout on commit", pr_comm.PROJECT_COMMITS[project],"for project",project
			branch_name = get_branch_name(tmp_build_path)
			branch = branch_name
	else:
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

		
	if os.path.isdir(build_path + utils.get_full_path(project, version, compiler)):
		shutil.rmtree(build_path + utils.get_full_path(project, version, compiler))
	shutil.move(tmp_build_path, build_path + utils.get_full_path(project, version, compiler))
	
	return version
	
	
def get_branch_name(path):
	p = subprocess.Popen(['git', '-C', path, 'rev-parse', '--abbrev-ref', 'HEAD'], close_fds = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	(stdout, stderr) = p.communicate()
	if p.returncode != 0:
		return (1,"")
	return (0, stdout.strip())
	
			
def get_status(path):
	p = subprocess.Popen(['git', '-C', path, 'status', '--porcelain'], close_fds = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	(stdout, stderr) = p.communicate()
	if p.returncode != 0:
		return 1
	elif len(stdout.strip()) != 0:
		return 1
	return 0

