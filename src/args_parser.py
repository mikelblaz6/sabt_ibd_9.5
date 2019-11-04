#! /usr/bin/python
import time, sys
import mrt_argparse
import defines as constants

from utils import print_error

def get_shell_args(shell_args):
    parser = mrt_argparse.ArgumentParser(description='Build MRT developments and dependencies.')
    parser.add_argument('-P', '--project', help='project to build', default = "")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-g', '--git', action='store_true', help='build from git sources')
    group.add_argument('-l', '--local', action='store_true', help='build from local sources (disables git)')
    parser.add_argument('-F', '--final-release', action='store_true', help='create final release storing version info in database. Includes -g -r -D -i -C -I, -P rootfs')
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('-d', '--debug', action='store_true', help='debug build')
    group2.add_argument('-r', '--release', action='store_true', help='release build')
    parser.add_argument('--no-cross-compile', action='store_true', help='x86 build')
    parser.add_argument('-D', '--compile-deps', action='store_true', help='rebuild all project dependencies')
    parser.add_argument('-m', '--make-params', help='arguments to be passed to final makefile of main project (if applies)', default = "")
    parser.add_argument('-c', '--create-only', action='store_true', help='only creates makefile and folder structure. Do not compile')
    parser.add_argument('-i', '--install', action='store_true', help='install project on install directory')
    #parser.add_argument('-C', '--clean-install-dir', action='store_true', help='clean install directory (only if install selected)')
    parser.add_argument('--no-rebuild', action='store_true', help='do not rebuild whole project (only if -l, and not -i and -D)')
    parser.add_argument('-I', '--images', action='store_true', help='create full tftp and web images, and incremental image')
    parser.add_argument('--fw-family', help='Fw Family', default = "NULL") 
    parser.add_argument('-V', '--final-release-version', help='set fw version for current release. Needed if --final-release active', default = "local")
    parser.add_argument('-M', '--previous-min-versions-list', help='Minimum fw version needed in RTU for compatibility with new fw. Needed if --final-release active. Format: [FW_FAMILY,MIN_VERSION;]', default = "local")
    parser.add_argument('--compiler', help='Compiler version (5/7)', default = "7")
    parser.add_argument('--part-number-list', help='Part number List', default = "NULL") 
    parser.add_argument('--legacy-mode', action='store_true', help='Produce fw packages for each part-number in part-number-list parameter')
    parser.add_argument('--legacy-min-versions', help='Min fw versions for each part-number in part-number-list', default="")
    parser.add_argument('--rc', help='Set number for Release candidate versions', default=None)
    return parser.parse_args(shell_args)


def get_paths(parsed_args):
    class Paths(object):
        __slots__ = ['work_path', 'build_path', 'deploy_path']
        
    paths = Paths()
    
    prefix = "local" if parsed_args.local else "git"
    date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    paths.work_path = constants.MAIN_DIR + 'builds/'+ prefix+ '/' + date
    
    cc_key = constants.ARM_TEMPLATE_SUFFIX if not parsed_args.no_cross_compile else constants.X86_TEMPLATE_SUFFIX
    deb_key = constants.DEBUG_TEMPLATE_SUFFIX if parsed_args.debug else constants.RELEASE_TEMPLATE_SUFFIX
    
    paths.build_path = constants.build_paths[cc_key][deb_key]
    paths.deploy_path = constants.deploy_paths[cc_key][deb_key]
    return paths


def normalize_args(parsed_args):
    
    if parsed_args.legacy_mode and parsed_args.legacy_min_versions == "":
        print_error("[--legacy-min-versions] needed if [--legacy-mode] set")
        raise Exception()
    
    if parsed_args.legacy_mode and \
        len(parsed_args.part_number_list.split(",")) != len(parsed_args.legacy_min_versions.split(",")):
        print_error("[--legacy-min-versions] and [--part-number-list] lengths must match")
        raise Exception()
    
    if parsed_args.final_release:
        if parsed_args.local:
            print("WARNING: [-l --local] option ignored")
        if parsed_args.debug:
            print("WARNING: [-d --debug] option ignored")
        if parsed_args.no_cross_compile:
            print("WARNING: [--no-cross-compile] option ignored")
        if parsed_args.create_only:
            print("WARNING: [-c] option ignored")
        if parsed_args.no_rebuild:
            print("WARNING: [--no-rebuild] option ignored")
            
            
        if parsed_args.final_release_version == "local":
            print_error("[-V --final-release-version] option required. Must be numeric")
            raise Exception()
        if parsed_args.previous_min_versions_list == "local":
            print_error("[-M --previous-min-versions] option required. Must be numeric")
            raise Exception()
        if parsed_args.part_number_list == "NULL":
            print_error("[--part-number-list] required for final release compilation")
            raise Exception()
        if parsed_args.fw_family == "NULL":
            print_error("[--fw-family] required for final release compilation")
            raise Exception()
        if parsed_args.compiler == "":
            print_error("[--compiler] required for final release compilation")
            raise Exception()
        
    
        parsed_args.project = "rootfs"
        parsed_args.compile_deps = True
        parsed_args.install = True
        parsed_args.images = True
        parsed_args.git = True
        parsed_args.release = True
        
    else:
        if parsed_args.project == "":
            print_error("[-P --project] option not set\n")
            raise Exception()

        if parsed_args.no_rebuild and (parsed_args.git or parsed_args.install or parsed_args.compile_deps):
            print_error("[--no-rebuild] option not compatible with other parameters ([-g --git], [-i --install], [-D --compile-deps])")
            raise Exception()
        
        '''if parsed_args.git and (not parsed_args.compile_deps or parsed_args.debug):
            sys.stderr.write("[-g --git] option not compatible with other parameters (no [-D --compile-deps], [-d --debug])")
            raise Exception()'''
            
        if parsed_args.install and (parsed_args.no_cross_compile or parsed_args.debug or parsed_args.create_only):
            print_error("[-I --images] option not compatible with other parameters ([--no-cross-compile], [-d --debug], [-c --create-only])")
            raise Exception()
            
        if parsed_args.images:
            parsed_args.install = True
        
        if parsed_args.images and (parsed_args.project != "rootfs"  or parsed_args.debug):
            print_error("[-I --images] option not compatible with other parameters ([-P --project] not rootfs, [-d --debug])")
            raise Exception()
            
        if parsed_args.images and (parsed_args.part_number_list == "NULL" or parsed_args.final_release_version == "local" \
			or parsed_args.previous_min_versions_list == "local" or parsed_args.compiler == "" or parsed_args.fw_family == "NULL"):
            print_error("[-I --images] option must include ([--part-number-list], [--fw-family], [-V --final-release-version], [-M --previous-min-version] and [--compiler])")
            raise Exception()
                         
    return parsed_args
