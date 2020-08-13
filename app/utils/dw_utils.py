# coding:utf8
from flask import make_response, send_file
from werkzeug.datastructures import ImmutableMultiDict
import datetime
from datetime import datetime as ddatetime, timedelta
import simplejson as json
from . import dw_const
import re
import xlwt
from conf.config import conf
import time
from functools import wraps
import hashlib
import sys
import collections
from app.utils import db_conn as db
import requests


def int5(x):
    if type(x) is str:
        x = float(x)
    y = int(x)
    if x - y > 0.4:
        return y + 1
    return y


def liststr2str(l):
    for x in ['[', ']', '(', ')', '"', "'", ' ']:
        l = l.replace(x, '')
    return ",".join(l.split(','))


def getDftValue(params, key, default='0'):
    val = params.get(key, default)
    if not val:
        return default
    if type(val) is str:
        return val.strip()
    else:
        return val


def tuple_dispose(alls):
    data = json.loads(alls)
    SAS = []
    for kv in data.items():
        SAS.append(kv)
    alls = ImmutableMultiDict(SAS)
    return alls


def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


def gbk2utf(in_data):
    return in_data.encode('gbk').decode('gbk')


def GetToday():
    '''#获取昨天日期'''
    today = datetime.date.today()
    return str(today).replace('-', '')


def GetCurrentTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def GetYesterday():
    '''#获取昨天日期'''
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return str(yesterday).replace('-', '')


def Getbeforeday(num):
    '''#获取昨天日期'''
    today = datetime.date.today()
    oneday = datetime.timedelta(days=num)
    yesterday = today - oneday
    return str(yesterday).replace('-', '')


def Yesterday(a):
    # load_week_data.py脚本使用函数
    today = ddatetime.now()
    price = today + timedelta(days=-a)
    return price


def Yesterdays(a):
    # load_week_data.py脚本使用函数
    today = ddatetime.now()
    price = today + timedelta(days=-a)
    return price.strftime("%Y%m%d")


def SafeInt(x, default=0):
    if not x:
        return default
    try:
        return int(x)
    except:
        return default


def ustr(s):
    if isinstance(s, unicode):
        return s.encode("utf8")
    try:
        return str(s)
    except:
        return ""


class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def toSuccessView(data):
    '''# 根据前端需要，定义成功返回json格式'''
    result = dict()
    result["code"] = 200
    result["message"] = ""
    result["data"] = data
    # print json.dumps(result,skipkeys=True,encoding='UTF-8'),'返回的数据以json格式进行展现'
    return json.dumps(result, skipkeys=True, encoding='UTF-8')


def SuccessData(code, message, data):
    result = dict()
    result["code"] = code
    result["message"] = message
    result["data"] = data
    return json.dumps(result, skipkeys=True, encoding='UTF-8')


def toSuccessViewNoResult(page, count=0, page_count=1):
    params = dict()
    params['page'] = page
    params['pageCount'] = page_count
    params['count'] = count
    params['records'] = []
    return toSuccessView(params)


def toErrorView(code, message, data):
    '''# 根据前端需要，定义错误返回json格式'''
    result = dict()
    result['code'] = code
    result['message'] = message
    result['data'] = False
    response = make_response(
        json.dumps(result, skipkeys=True, encoding='UTF-8'))
    if code == '100' or code == 100:
        response.set_cookie("username", "", expires=0)
        response.set_cookie("user_id", "", expires=0)
        response.set_cookie("session", "", expires=0)
        response.set_cookie("", "", expires=0)
    return response


def pageCount(count, pagesize):
    '''# 根据前端需要，定义分页页数'''
    return (count / pagesize) if (count %
                                  pagesize == 0) else (count / pagesize) + 1


def MyIsDigit(s):
    try:
        int(s)
    except:
        return False
    return True


map_dict = {
    14000003: "1,",
    14000005: "2,",
    14000098: "3,",
    14000008: "4,",
    14000014: "5,",
    22000001: "6,",
    22000002: "7,",
    25000001: "8,",
    25000002: "9,",
    21000001: "10,",
    21000002: "11,",
    21000003: "12,",
    21000004: "13,",
    50000004: "14,",
    50000001: "15,",
    80000091: "16,",
    80000092: "17,",
    27000004: "18,",
    27000005: "19,",
    27000006: "20,",
    60000010: "21,",
    60000001: "22,",
    60000012: "23,",
    60000013: "24,",
    80000089: "25,",
    14000045: "26,",
    80000055: "27,",
    80000056: "28,",
    80000013: "29,",
    14000015: "30,",
    80000057: "31,",
    80000058: "32,"
}


def behaviors(figures):
    joins = ''
    behaviors_dict = {
        1: "转发",
        2: "评论",
        3: "点赞",
        4: "关注",
        5: "短链点击",
        6: "图文card描述区域点击",
        7: "图文card按钮点击",
        8: "视频card描述区域点击",
        9: "视频card按钮点击",
        10: "头像点击",
        11: "昵称点击",
        12: "@点击",
        13: "话题点击",
        14: "图片点击",
        15: "正文点击",
        16: "视频点击",
        17: "3S以上视频自动播放",
        18: "图片横滑",
        19: "图片标签点击",
        20: "图片按钮点击",
        21: "banner图片点击",
        22: "橱窗点击",
        23: "banner按钮点击",
        24: "banner标题点击",
        25: "边看边下(视频点击播放)",
        26: "收藏博文",
        27: "视频内置按钮点击",
        28: "左滑进落地页",
        29: "左滑进个人主页",
        30: "置顶评论短链点击",
        31: "点击头像进落地页",
        32: "点击视频Card弹窗进入落地页"
    }
    for i in figures:
        joins += behaviors_dict[i] + '/'
    return joins


def wipeOff(_params):
    lens = len(_params)
    box = []
    d = 0
    a = ''
    for row in _params:
        d += 1
        if str(row) != ',':
            a += str(row)
        if row == ',' or d == lens:
            box.append(int(a))
            a = ''
    return box


def insert_data_function(system):
    if system == '0':
        return '不限'
    elif system == '1':
        return 'ios'
    elif system == '2':
        return 'Android'


def log_path():
    f_back = sys._getframe().f_back.f_back
    funcName = f_back.f_code.co_name
    fileName = f_back.f_code.co_filename
    if 'Data-web/' in str(fileName):  # api接口
        s = 'API.' + str(funcName)
        return s
    else:
        s = 'SCRIPT.' + str(fileName)
        return s


def md5(item):
    if item is None:
        return ''
    elif len(item) == '32':
        return item
    elif len(item) < 5:
        return ''
    elif item == '00000000-0000-0000-0000-000000000000':
        return ''
    else:
        m = hashlib.md5()
        m.update(item)
        return m.hexdigest()


def activate_time(start):
    y = ddatetime.strptime(start, "%Y-%m-%d")
    price = y + timedelta(days=8)
    return price.strftime("%Y%m%d")


# 结束时间扩大30天，把延迟数据全都进行统计
def BETWEEN_time(start):
    y = ddatetime.strptime(start, "%Y-%m-%d")
    price = y + timedelta(days=30)
    return price.strftime("%Y%m%d")


def fs_time(start, num):
    y = ddatetime.strptime(start, "%Y-%m-%d")
    price = y + timedelta(days=num)
    return price.strftime("%Y%m%d")


def fs(start, end):
    timeList = []
    num = 0
    while True:
        start = start[0:4] + '-' + start[4:6] + '-' + start[6:8]
        start = fs_time(start, num)
        if start <= end:
            timeList.append(int(start))
            num = 1
        else:
            break
    return timeList


def underline2Hump(one_string, space_character):
    '''#将下划线命名转为驼峰命名'''
    # one_string:输入的字符串；space_character:字符串的间隔
    # 将字符串转化为list
    string_list = str(one_string).split(space_character)
    first = string_list[0].lower()
    others = string_list[1:]
    # str.capitalize():将字符串的首字母转化为大写
    others_capital = [word.capitalize() for word in others]
    others_capital[0:0] = [first]
    # 将list组合成为字符串，中间无连接符
    hump_string = ''.join(others_capital)
    return hump_string


# 将驼峰转为下划线命名
def replaceHump(match):
    if match:
        line_fore, line_back = match.groups()
        if len(line_back) == 1:
            line_back = line_back.lower()
        return '_'.join([line_fore, line_back])


# 调用 replace_hump 函数 将驼峰转为下划线命名


def hump2Line(strtf):
    ret = re.sub(r'([a-z])([A-Z]+)', replaceHump, strtf)
    # return re.sub(r"\d+","_1",ret)
    return ret.replace("1", "_1")


def sort_filed(argsSort):
    del_blank = argsSort.strip()
    del_blank = del_blank.replace(',', '')
    ff = del_blank.split(' ', 2)
    if len(ff) == 2:
        if 'rate' in str(ff[0]):
            field = ",({0}*100) {1}".format(ff[0], ff[1])
        else:
            field = ",convert({0},decimal(12,2)) {1}".format(ff[0], ff[1])
        return field
    else:
        return ''


def OutFormatDate(date):
    return date[:4] + '-' + date[4:6] + '-' + date[6:]


def group_dispose(group_by):
    txt = group_by.replace(' GROUP BY ', '')
    x = txt.split(",", 10)
    key = ''
    lens = len(x) - 1
    for index, i in enumerate(x):
        if index == lens:
            key += "str(row['{0}'])".format(i)
        else:
            key += "str(row['{0}']) + '-' +".format(i)
    return key


def ExportExcelSheets(filename, tables):
    wbk = xlwt.Workbook()
    for table in tables:
        sheet = wbk.add_sheet(table[0], cell_overwrite_ok=True)
        for idx, table_title in enumerate(table[1][0]):
            sheet.write(0, idx, table_title[1])
        for idxi, row in enumerate(table[1][1]):
            for idxj, table_title in enumerate(table[1][0]):
                if row.has_key(table_title[0]):
                    val = row[table_title[0]]
                    if table_title[
                            2] == dw_const.COLUMN_TYPE.CENT and MyIsDigit(
                                str(val)):
                        val = str(int(val) / 100.00)
                    elif table_title[
                            2] == dw_const.COLUMN_TYPE.PERCENT and MyIsDigit(
                                str(val)):
                        val = str(int(val) / 100.00) + "%"
                    sheet.write(idxi + 1, idxj, u'%s' % (val))
                else:
                    sheet.write(idxi + 1, idxj, u"/")
    path = conf.OUT_FILE_PATH  # r'/data2/project/Data-web/'
    tableName = filename + ".xls"
    wbk.save(path + tableName)
    response = make_response(send_file(path + tableName))
    response.headers["Content-Disposition"] = "attachment; filename=" + \
        tableName.encode('utf8') + ";"
    return response


def ExportExcel(records, table_titles, exportName):
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    for idx, table_title in enumerate(table_titles):
        sheet.write(0, idx, table_title[1])
    for idxi, row in enumerate(records):
        for idxj, table_title in enumerate(table_titles):
            if row.has_key(table_title[0]):
                val = row[table_title[0]]
                if table_title[2] == dw_const.COLUMN_TYPE.CENT and MyIsDigit(
                        str(val)):
                    val = str(int(val) / 100.00)
                elif table_title[
                        2] == dw_const.COLUMN_TYPE.PERCENT and MyIsDigit(
                            str(val)):
                    val = str(int(val) / 100.00) + "%"
                sheet.write(idxi + 1, idxj, u'%s' % (val))
            else:
                sheet.write(idxi + 1, idxj, u"/")
    path = conf.OUT_FILE_PATH  # r'/data2/project/Data-web/'
    # tableName = str(int(time.time())) + ".xls"
    tableName = exportName + ".xls"
    wbk.save(path + tableName)
    response = make_response(send_file(path + tableName))
    response.headers["Content-Disposition"] = "attachment; filename=" + \
        tableName.encode('utf8') + ";"
    return response


def ExportExcelAdUse(records, table_titles, exportName):
    # 暂时拷贝上述的导出代码 理由是 数据单位不一致
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    for idx, table_title in enumerate(table_titles):
        sheet.write(0, idx, table_title[1])
    for idxi, row in enumerate(records):
        for idxj, table_title in enumerate(table_titles):
            if row.has_key(table_title[0]):
                val = row[table_title[0]]
                if table_title[2] == dw_const.COLUMN_TYPE.CENT and MyIsDigit(
                        val):
                    val = str(round(val, 2))
                elif table_title[
                        2] == dw_const.COLUMN_TYPE.PERCENT and MyIsDigit(val):
                    # print(table_title,val)
                    val = float(val)
                    val = str(round(val * 100.00, 2)) + "%"
                sheet.write(idxi + 1, idxj, u'%s' % (val))
            else:
                sheet.write(idxi + 1, idxj, u"-")
    path = conf.OUT_FILE_PATH  # r'/data2/project/Data-web/'
    tableName = str(exportName) + ".xls"
    wbk.save(path + tableName)
    response = make_response(send_file(path + tableName))
    response.headers["Content-Disposition"] = "attachment; filename=" + \
        tableName.encode('utf8') + ";"
    return response


def wirite_files(newListSms, id, dateType, resourceID, DATAtype, lists):
    if dateType == '0':
        newListSms.sort(key=lambda x: x['p_date'])
    # print newListSms
    times = '汇总'
    if dateType == '0':  # 汇总没有日期
        times = '日期'
    export_name = dw_const.dataType_dict[DATAtype]
    names = dw_const.dataType_dict[DATAtype]
    filename = str(id) + '.xls'
    if resourceID == '1' and DATAtype == '2':
        export_name = '互动量(微博)'
    elif resourceID == '1' and DATAtype == '3':
        export_name = '点击量(微博)'
    elif resourceID != '1' and DATAtype == '2':
        export_name = '互动量(其它)'
    elif resourceID != '1' and DATAtype == '3':
        export_name = '点击量(其它)'
    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet(export_name, cell_overwrite_ok=True)
    sheet.write(0, 0, times)
    if dateType == '1':
        for i, j in enumerate(newListSms):
            if lists == []:  # 汇总没有行为
                sheet.write(0, 1, names)
                sheet.write(1, 0, j['p_date'])
                sheet.write(1, i + 1, j['sum'])
            else:
                sheet.write(1, 0, j['p_date'])
                sheet.write(0, i + 1, j['is'])
                sheet.write(1, i + 1, j['sum'])
    elif dateType == '0' and lists == []:
        for i, j in enumerate(newListSms):
            sheet.write(0, 1, names)
            sheet.write(i + 1, 0, j['p_date'])
            sheet.write(i + 1, 1, j['sum'])
    else:
        list1 = []
        a = []
        for i, xjds in enumerate(newListSms):
            if xjds['is'] not in a:
                a.append(xjds['is'])
                params = []
                for j, xjd in enumerate(newListSms):
                    if xjds['is'] == xjd['is']:
                        params.append(xjd)
                list1.append(params)
            else:
                break
        for i, table in enumerate(list1):
            for j, xjd in enumerate(table):
                sheet.write(0, i + 1, xjd['is'])
                sheet.write(j + 1, i + 1, xjd.get('sum', 0))
                sheet.write(j + 1, 0, xjd.get('p_date', 0))
    path = conf.file_path
    tableName = filename
    wbk.save(path + tableName)


@singleton
class realtime_section(object):
    def __init__(self):
        self._last_load = time.time()
        self._bid_req_cnt_tables = {}
        self._tax_pid_resid_map = {}
        # self._bid_req_cnt_datas = {}
        sql = 'select platform_id,stream_table_name,resource_map,resource_id from tdw_resource_map where del =0'
        rows = db.SQL_DW(sql)
        for row in rows:
            self._tax_pid_resid_map[int(
                row['resource_id'])] = row["platform_id"]
            # self._bid_req_cnt_datas[int(row['platform_id'])] = {}
            if str(row['resource_map']) == '1':
                self._bid_req_cnt_tables[int(row['platform_id'])] = {
                    int(row['resource_id']): str(row['stream_table_name'])
                }
            else:
                self._bid_req_cnt_tables[int(row['platform_id'])] = str(
                    row['stream_table_name'])

    # 每隔５分钟初始化一下数据库
    def tables(self):
        if time.time() - self._last_load > 300:
            self.__init__()
        return self._bid_req_cnt_tables

    def maps(self):
        return self._tax_pid_resid_map

    # def datas(self):
    #     return self._bid_req_cnt_datas


resource_update_data = realtime_section()


@singleton
class week_sort(object):
    def __init__(self):
        self._last_load = time.time()
        self._sort_dict = {}
        self._SUM_sort = {}
        self._sort_dict = collections.OrderedDict()
        self._SUM_sort = collections.OrderedDict()
        sql = 'select sort_id,platform_id from tdw_resource_map where platform_id != 1001 ORDER BY sort_id '
        rows = db.SQL_DW(sql)
        for row in rows:
            self._sort_dict[row['sort_id']] = row['platform_id']
            self._SUM_sort[row['platform_id']] = row['sort_id']

    # 每隔５分钟初始化一下数据库
    def platform(self):
        if time.time() - self._last_load > 300:
            self.__init__()
        return self._sort_dict

    def consume(self):
        self._SUM_sort[-3] = 100
        return self._SUM_sort


week_views_sort = week_sort()

