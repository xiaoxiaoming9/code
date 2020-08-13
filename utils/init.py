# coding:utf8
import dw_utils
import db_conn as db
import dw_const
import time
import collections


@dw_utils.singleton
class Channels(object):
    def __init__(self):
        self._last_load = time.time()
        self._cd = dict()
        sql = "select * from t_channel"
        rows = db.SQL_DW(sql)
        for row in rows:
            self._cd[row['c_id']] = row['c_name']

    def ids(self):
        cd = dict()
        sql = "select * from t_channel where status=0 "
        rows = db.SQL_DW(sql)
        for row in rows:
            cd[row['c_id']] = row['c_name']
        return cd

    def __getitem__(self, key):
        if time.time() - self._last_load > 60:
            self.__init__()
        if not self._cd.has_key(key):
            return ""
        return self._cd[key]


@dw_utils.singleton
class Business(object):
    def __init__(self):
        self._bd = dict()
        sql = "select * from wead_inner_business"
        rows = db.SQL_BI(sql)
        for row in rows:
            self._bd[str(row['business_id'])] = row['business_name']

    def ids(self):
        return self._bd

    def __getitem__(self, key):
        key = str(key)
        if not self._bd.has_key(key):
            return "其他"
        return self._bd[key]





# 多个类引用此装饰器，其内部已经实现了区分，相当与
class lazy(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


class Resource(object):
    def __init__(self):
        self.resource = dict()

    @lazy
    def mapData(self):
        # 这里只会执行一次,可以有效防止每次调用都进行sql的查询
        sql = 'select * from tdw_resource_map where del =0'
        rows = db.SQL_DW(sql)
        for row in rows:
            self.resource[int(row['resource_id'])] = row['platform_id']
        return self.resource


@dw_utils.singleton
class Cloud(object):
    def __init__(self):
        self._start_time = time.time()
        self._cd = dict()
        sql = 'select saas_id,company_name from t_channel where status=0 group by saas_id'
        rows = db.SQL_DW(sql)
        for row in rows:
            self._cd[row['saas_id']] = row['company_name']

    # 选择框有5分钟延迟,也可以在这里调用初始化方法解决延迟
    def ids(self):
        return self._cd

    def __getitem__(self, key):
        if time.time() - self._start_time > 300:
            self.__init__()
        # if self._cd.get(key) is None:
        #     self.__init__()
        return self._cd.get(key, '其它')




@dw_utils.singleton
class resourceKeyName(object):
    def __init__(self):
        self._last_load = time.time()
        self._cd = dict()
        self._cd = collections.OrderedDict()
        sql = 'select resource_id,platform_name from tdw_resource_map where del=0 GROUP BY sort_id'
        rows = db.SQL_DW(sql)
        for row in rows:
            self._cd[row['resource_id']] = row['platform_name']

    def appId(self):
        return self._cd

    def __getitem__(self, key):
        if time.time() - self._last_load > 300:
            self.__init__()
        return self._cd.get(key)


resource_data = Resource()
dw_const.resource_map = resource_data.mapData
dw_const.CLOUD = Cloud()
dw_const.PID_NEW_NAMES = Platfrom()
dw_const.CHANNELS = Channels()


