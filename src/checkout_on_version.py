#! /usr/bin/python
import time, sys, os
import mrt_argparse
import defines as constants
import mrt_git
import database
import ConfigParser
from utils import print_error

def get_shell_args(shell_args):
    parser = mrt_argparse.ArgumentParser(description='Checkout local sources from main project version')
    parser.add_argument('-v', '--project-version', help='version')
    parser.add_argument('--fw-family', help='Fw family', default="NULL")
    parser.add_argument('--part-number', help='Part number')
    return parser.parse_args(shell_args)
    

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


def prepare_local(project, version, part_number):
    source_path = search_project_path(project) + project
    if version == "final":
        branch_name = ''
        #=======================================================================
        # for branch in constants.GIT_BRANCHES:
        #     if mrt_git.checkout(source_path, branch) == 0:
        #         print "Checking out sources for project", project, ". Branch", branch, ". Path", source_path
        #         branch_name = branch
        #         break
        # if branch_name == '':
        #     print "ERROR checking out project", project, "on branch. ABORTING"
        #     exit(1)
        #=======================================================================
    else:
        commit_id = 0
        sql = database.Database()
        if constants.GLOBAL_PROJECT == 'NULL':
            commit_id = sql.GetCommitByVersionPartNumber(project, part_number, version)
        else:
            commit_id = sql.GetCommitByVersionFamily(project, constants.GLOBAL_PROJECT, version)
        sql.quit()
        print "Checking out sources for project", project, ". Commit", commit_id, ". Path", source_path

        if mrt_git.checkout(source_path, commit_id):
            print "ERROR checking out project", project, ". ABORTING"
            exit(1)

    return source_path


class Dependencies:
    def __init__(self, args):
        self.main_project = "rootfs"
        self.project_tree = {}
        self.git_last_versions = {}
        self.version = args.project_version
        self.part_number = args.part_number
    
    def get_depend_projects(self):
        self.get_depend_projects_iter(self.main_project, self.version)

    # Funcion recursiva que recorre todo el arbol de dependencias
    def get_depend_projects_iter(self, project, version):
        try:
            project_path = ""
            if not project in self.project_tree:
                self.project_tree[project] = {}
                project_path = prepare_local(project, version, self.part_number)
            else:
                return

            cfg = ConfigParser.RawConfigParser(allow_no_value=True)
            cfg.optionxform=str
            cfg.read(project_path + '/mrt/project')
            
            self.project_tree[project][version] = {'provides':[], 'depends':[], 'install_depends':[]}
            for prov in cfg.items('PROVIDES'):
                self.project_tree[project][version]['provides'].append(prov[0])
            if cfg.has_section('INSTALL_DEPS'):
                for fdep in cfg.items('INSTALL_DEPS'):
                    self.project_tree[project][version]['install_depends'].append(fdep[0])
                    
            if cfg.has_section('DEPS'):
                for dependency in cfg.items('DEPS'):
                    #Not version checking. Version set to None
                    if not dependency[0] in self.project_tree[project][version]['depends']:
                        self.project_tree[project][version]['depends'].append(dependency[0])
                    self.get_depend_projects_iter(dependency[0], version)
        except Exception as inst:
            #logger.error("Error getting dependencies for project " + str(project) + ", version " + str(version) + ". Exception: " + str(inst))
            print_error("Error getting dependencies for project " + str(project) + ", version " + str(version) + ". Exception: " + str(inst))
            raise Exception()


def doit(args):
    constants.set_GLOBAL_PROJECT("NULL", args.fw_family, "local")
    dep_processor_chk = Dependencies(args)
    dep_processor_chk .get_depend_projects()
    

    
if __name__ == '__main__':
    args = get_shell_args(sys.argv[1:])
    doit(args)
