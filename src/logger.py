#! /usr/bin/python
import logging, os

ready = False


def init(args, paths):
    global ready
    os.system('mkdir -p ' + paths.work_path)
    filename = paths.work_path + '/log.txt'
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
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