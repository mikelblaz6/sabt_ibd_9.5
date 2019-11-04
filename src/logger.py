#! /usr/bin/python
import logging, os

ready = False

def get_filename(args, paths):
    return paths.work_path + '/' + args.fw_family + '_' + args.final_release_version  + '_log.txt'


def init(args, paths):
    global ready
    os.system('mkdir -p ' + paths.work_path)
    filename = get_filename(args, paths)
    logging.basicConfig(filename=filename, format='%(message)s', level=logging.DEBUG)
    logging.info("Starting app")
    logging.info("Invoked with arguments: " + str(args))
    ready = True
    
def error(data):
    if ready:
        logging.error(data)
    
def warning(data):
    if ready:
        logging.warning(data)
    
def info(data):
    if ready:
        logging.info(data)
    
def debug(data):
    if ready:
        logging.debug(data)