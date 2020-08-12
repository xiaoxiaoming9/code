# coding:utf-8
import traceback
from logging import getLogger, INFO
from cloghandler import ConcurrentRotatingFileHandler
from conf.config import conf
import os
import datetime
import socket
from functools import wraps


def get_local_ip():
    ret = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ret.connect(('8.8.8.8', 80))
    ip = ret.getsockname()[0]
    return ip


try:
    ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
except:
    ip = get_local_ip()


class logger(object):
    def __init__(self, path, info):
        log = getLogger(info)
        logfile = os.path.abspath(path)
        rotateHandler = ConcurrentRotatingFileHandler(logfile, "a",
                                                      300 * 1024 * 1024, 10)
        log.addHandler(rotateHandler)
        log.setLevel(INFO)
        self._log = log

    def log(self, mark, brief, msg):
        data = str(datetime.datetime.now()
                   ) + " INFO " + ip + " {mark} - {brief}; {msg}".format(
                       mark=mark, brief=brief, msg=msg)
        self._log.info(data)

    def error(self, mark, brief, msg):
        data = str(datetime.datetime.now()
                   ) + " ERROR " + ip + " {mark} - {brief}; {msg}".format(
                       mark=mark, brief=brief, msg=msg)
        self._log.info(data)

    def debug(self, mark, brief, msg):
        data = str(datetime.datetime.now()
                   ) + " DEBUG " + ip + " {mark} - {brief}; {msg}".format(
                       mark=mark, brief=brief, msg=msg)
        self._log.info(data)

    def info(self, mark, brief, msg):
        data = str(datetime.datetime.now()
                   ) + " INFO " + ip + " {mark} - {brief}; {msg}".format(
                       mark=mark, brief=brief, msg=msg)
        self._log.info(data)

    def warn(self, mark, brief, msg):
        data = str(datetime.datetime.now()
                   ) + " WARN " + ip + " {mark} - {brief}; {msg}".format(
                       mark=mark, brief=brief, msg=msg)
        self._log.info(data)


all_logger = logger(conf.log_all_file_path, "all")
err_logger = logger(conf.log_error_file_path, "error")
warn_logger = logger(conf.log_warn_file_path, "warn")

log_dict = {"all": all_logger, "err": err_logger, "warn": warn_logger}


def getLog(info):
    l = log_dict.get(info)
    if not l:
        l = logger(conf.log_path + info + ".log", info)
        log_dict.update({info: l})
    return l


info = all_logger.info
error = err_logger.error
warn = warn_logger.warn
log = all_logger.log
section_error = warn_logger.error
section_log = warn_logger.log

#####
if conf.DEBUG:
    debug = all_logger.debug
else:

    def debug(a, b, c):
        pass


def run_safe(_func):
    @wraps(_func)
    def wraper(*args, **kwargs):
        try:
            return _func(*args, **kwargs)
        except Exception as e:
            error("API.{0}".format(_func.__name__), e, traceback.format_exc())
            raise e

    return wraper


def script_run_safe(_func):
    @wraps(_func)
    def wraper(*args, **kwargs):
        try:
            return _func(*args, **kwargs)
        except Exception as e:
            err = traceback.format_exc()
            error("SCRIPT.{0}".format(_func.__name__), '脚本执行出现错误', err)
            raise e

    return wraper


