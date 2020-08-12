# coding:utf8
from ..utils import dw_utils, db_conn as db, dw_const
import collections




def listPlatformWeAD(_params):
    sql = 'select platform_id,platform_name,del from tdw_resource_map where platform_id !=0 ORDER BY sort_id'
    rows = db.SQL_DW(sql)
    output = []
    params = {}
    params = collections.OrderedDict()
    rests = {'id': 100, 'name': '其它', 'childen': []}
    for row in rows:
        rd = dw_utils.Dict()
        rd.id = row['platform_id']
        rd.name = row['platform_name']
        if row['del'] == 1:
            rests['childen'].append(rd)
        else:
            output.append(rd)
    output.append(rests)
    params['count'] = len(output)
    params['records'] = output
    return dw_utils.toSuccessView(params)


