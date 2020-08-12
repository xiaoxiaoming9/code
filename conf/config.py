# coding:utf-8
import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding("utf-8")


class ConfigParse(object):
    def getFilePath(self, name=""):
        from os import path
        d = path.dirname(__file__)
        if name == "":
            newpath = "/resources/app.conf"
        else:
            newpath = "/resources/app-{0}.conf".format(name)
        p = d.replace("/conf", newpath)
        return p

    def getFileName(self):
        p = self.getFilePath()
        cf = ConfigParser.ConfigParser()
        cf.read(p)
        name = cf.get("app", "app")
        return name

    def save(self):
        name = self.getFileName()
        path = self.getFilePath(name)
        cf = ConfigParser.ConfigParser()
        cf.read(path)
        self.cf = cf

    def parse(self, section, key):
        return self.cf.get(section, key)


class ConfigNew(object):
    parse = ConfigParse()
    parse.save()
    log_all_file_path = parse.parse("logfile", "log_all_file_path")
    log_error_file_path = parse.parse("logfile", "log_error_file_path")
    log_warn_file_path = parse.parse("logfile", "log_warn_file_path")
    log_path = parse.parse("logfile", "log_path")
    file_path = parse.parse("filepath", "file_path")
    save_path = parse.parse("filepath", "save_path")
    OUT_FILE_PATH = parse.parse("filepath", "OUT_FILE_PATH")
    data_package_path = parse.parse("filepath", "data_package")
    BI_HOST = parse.parse("wead_dsp_stat", "BI_HOST")
    BI_USER = parse.parse("wead_dsp_stat", "BI_USER")
    BI_PASSWORD = parse.parse("wead_dsp_stat", "BI_PASSWORD")
    BI_DATABASE = parse.parse("wead_dsp_stat", "BI_DATABASE")
    BI_PORT = int(parse.parse("wead_dsp_stat", "BI_PORT"))
    BI_CHARSET = parse.parse("wead_dsp_stat", "BI_CHARSET")
    DSP_HOST = parse.parse("dsp", "DSP_HOST")
    DSP_USER = parse.parse("dsp", "DSP_USER")
    DSP_PASSWORD = parse.parse("dsp", "DSP_PASSWORD")
    DSP_DATABASE = parse.parse("dsp", "DSP_DATABASE")
    DSP_PORT = int(parse.parse("dsp", "DSP_PORT"))
    DSP_CHARSET = parse.parse("dsp", "DSP_CHARSET")

    DW_HOST = parse.parse("data_web", "DW_HOST")
    DW_USER = parse.parse("data_web", "DW_USER")
    DW_PASSWORD = parse.parse("data_web", "DW_PASSWORD")
    DW_DATABASE = parse.parse("data_web", "DW_DATABASE")
    DW_PORT = int(parse.parse("data_web", "DW_PORT"))
    DW_CHARSET = parse.parse("data_web", "DW_CHARSET")

    CELERY_BROKER_URL = parse.parse("redis", "CELERY_BROKER_URL")

    COUNT_HOST = parse.parse("count", "COUNT_HOST")
    COUNT_USER = parse.parse("count", "COUNT_USER")
    COUNT_PASSWORD = parse.parse("count", "COUNT_PASSWORD")
    COUNT_DATABASE = parse.parse("count", "COUNT_DATABASE")
    COUNT_PORT = int(parse.parse("count", "COUNT_PORT"))
    COUNT_CHARSET = parse.parse("count", "COUNT_CHARSET")

    USER_PORTRAYAL_TABLE = parse.parse("odps", "USER_PORTRAYAL_TABLE")
    access_id = parse.parse("odps", "access_id")
    secret_access_key = parse.parse("odps", "secret_access_key")
    project = parse.parse("odps", "project")
    SMS_CODE_TEMP_ID = parse.parse("odps", "SMS_CODE_TEMP_ID")
    tunnel = parse.parse("odps", "tunnel")
    DEBUG = True if parse.parse("debug", "debug") == "True" else False


conf = ConfigNew()
DEBUG = conf.DEBUG
