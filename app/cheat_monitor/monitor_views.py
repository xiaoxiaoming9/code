# coding:utf-8
from app.utils import dw_utils, dw_const, db_conn as db, sql_utils, log


@log.run_safe
def monitor_hour(_params):
    resourceID = dw_utils.getDftValue(_params, 'resourceID', "-2")
    times = dw_utils.getDftValue(_params, 'times', "0")
    page = dw_utils.getDftValue(_params, 'page', 1)
    start = (int(page) - 1) * dw_const.DEFAULT_PAGE_SIZE
    export = dw_utils.getDftValue(_params, 'export', False)
    date = dw_utils.OutFormatDate(dw_utils.Yesterdays(0))
    st = dw_utils.getDftValue(_params, 'startDate', date)
    et = dw_utils.getDftValue(_params, 'endDate', date)
    st = st.replace("-", "")
    et = et.replace("-", "")
    argsSort = sql_utils.orderBySql(_params)

    sql = "select dates,resource_id,req_cnt,req_sum,req_user,concat(times-1,':00','~',CAST(times AS SIGNED integer ),':00') as times from bid_req_filter_stat_hour where dates>='{0}' AND dates<='{1}'".format(
        st, et)
    count_sql = "select count(1) as count1 from bid_req_filter_stat_hour where dates>='{0}' AND dates<='{1}'".format(
        st, et)
    if resourceID != '-2':
        a_sql = ' AND resource_id={0}'.format(resourceID)
        sql = sql + a_sql
        count_sql = count_sql + a_sql

    if times != '0':
        b_sql = ' AND times={0}'.format(times)
        sql += b_sql
        count_sql += b_sql
    sql = sql + " ORDER BY 1=1" + argsSort
    if not export:
        sql = "select * from({0})a".format(
            sql) + " limit %s,%s" % (start, dw_const.DEFAULT_PAGE_SIZE)
    # print sql
    entries = []
    rows = db.SQL_BI(sql)
    for row in rows:
        rd = dw_utils.Dict()
        rd.dates = row['dates']
        rd.times = row['times']
        platformName = dw_const.resourceName[row['resource_id']]
        if platformName is None:
            continue
        rd.platformName = platformName
        rd.reqUser = '{:,.0f}'.format(row['req_user'])
        rd.reqCnt = '{:,.0f}'.format(row['req_cnt'])
        rd.reqSum = '{:,.0f}'.format(row['req_sum'])
        entries.append(rd)
    if export:
        exportName = '流量过滤监测时表' + str(st)
        table_titles = [("dates", u"日期", dw_const.COLUMN_TYPE.STRING),
                        ("times", u"时间", dw_const.COLUMN_TYPE.STRING),
                        ("platformName", u"资源", dw_const.COLUMN_TYPE.STRING),
                        ("reqUser", u"过滤用户", dw_const.COLUMN_TYPE.STRING),
                        ("reqCnt", u"过滤请求量", dw_const.COLUMN_TYPE.STRING),
                        ("reqSum", u"过滤广告位数量", dw_const.COLUMN_TYPE.STRING)]
        return dw_utils.ExportExcel(entries, table_titles, exportName)
    count_result = db.SQL_BI(count_sql)
    count = count_result[0]['count1'] if len(count_result) > 0 else 0
    params = dict()
    params['page'] = page
    params['pageCount'] = dw_utils.pageCount(int(count),
                                             dw_const.DEFAULT_PAGE_SIZE)
    params['count'] = count
    params['records'] = entries
    return dw_utils.toSuccessView(params)


@log.run_safe
def monitor_day(_params):
    resourceID = dw_utils.getDftValue(_params, 'resourceID', "-2")
    page = dw_utils.getDftValue(_params, 'page', 1)
    start = (int(page) - 1) * dw_const.DEFAULT_PAGE_SIZE
    export = dw_utils.getDftValue(_params, 'export', False)
    date = dw_utils.OutFormatDate(dw_utils.Yesterdays(1))
    st = dw_utils.getDftValue(_params, 'startDate', date)
    et = dw_utils.getDftValue(_params, 'endDate', date)
    st = st.replace("-", "")
    et = et.replace("-", "")
    argsSort = sql_utils.orderBySql(_params)

    sql = "select * from bid_req_filter_stat_day where dates>='{0}' AND dates<='{1}'".format(
        st, et)
    count_sql = "select count(1) as count1 from bid_req_filter_stat_day where dates>='{0}' AND dates<='{1}'".format(
        st, et)
    if resourceID != '-2':
        a_sql = ' AND resource_id={0}'.format(resourceID)
        sql = sql + a_sql
        count_sql = count_sql + a_sql
    sql = sql + " ORDER BY 1=1" + argsSort
    if not export:
        sql = "select * from({0})a".format(
            sql) + " limit %s,%s" % (start, dw_const.DEFAULT_PAGE_SIZE)
    entries = []
    rows = db.SQL_BI(sql)
    for row in rows:
        rd = dw_utils.Dict()
        rd.dates = row['dates']
        platformName = dw_const.resourceName[row['resource_id']]
        if platformName is None:
            continue
        rd.platformName = platformName
        rd.reqUser = '{:,.0f}'.format(row['req_user'])
        rd.reqCnt = '{:,.0f}'.format(row['req_cnt'])
        rd.reqSum = '{:,.0f}'.format(row['req_sum'])
        entries.append(rd)
    if export:
        exportName = '流量过滤监测日表' + str(st)
        table_titles = [("dates", u"日期", dw_const.COLUMN_TYPE.STRING),
                        ("platformName", u"资源", dw_const.COLUMN_TYPE.STRING),
                        ("reqUser", u"过滤用户", dw_const.COLUMN_TYPE.STRING),
                        ("reqCnt", u"过滤请求量", dw_const.COLUMN_TYPE.STRING),
                        ("reqSum", u"过滤广告位数量", dw_const.COLUMN_TYPE.STRING)]
        return dw_utils.ExportExcel(entries, table_titles, exportName)
    count_result = db.SQL_BI(count_sql)
    count = count_result[0]['count1'] if len(count_result) > 0 else 0
    params = dict()
    params['page'] = page
    params['pageCount'] = dw_utils.pageCount(int(count),
                                             dw_const.DEFAULT_PAGE_SIZE)
    params['count'] = count
    params['records'] = entries
    return dw_utils.toSuccessView(params)


@log.run_safe
def blacklist_collect(_params):
    page = dw_utils.getDftValue(_params, 'page', 1)
    start = (int(page) - 1) * dw_const.DEFAULT_PAGE_SIZE
    export = dw_utils.getDftValue(_params, 'export', False)
    date = dw_utils.OutFormatDate(dw_utils.Yesterdays(1))
    st = dw_utils.getDftValue(_params, 'startDate', date)
    et = dw_utils.getDftValue(_params, 'endDate', date)
    st = st.replace("-", "")
    et = et.replace("-", "")
    argsSort = sql_utils.orderBySql(_params)

    sql = "select * from ab_fake_device_stat where dates>='{0}' AND dates<='{1}'".format(
        st, et)
    count_sql = "select count(1) as count1 from ab_fake_device_stat where dates>='{0}' AND dates<='{1}'".format(
        st, et)
    sql = sql + " ORDER BY 1=1" + argsSort
    if not export:
        sql = "select * from({0})a".format(
            sql) + " limit %s,%s" % (start, dw_const.DEFAULT_PAGE_SIZE)
    entries = []
    rows = db.SQL_BI(sql)
    for row in rows:
        rd = dw_utils.Dict()
        rd.dates = row['dates']
        rd.deviceNum = '{:,.0f}'.format(row['device_num'])
        rd.addNum = '{:,.0f}'.format(row['add_device_num'])
        rd.userNum = '{:,.0f}'.format(row['user_num'])
        rd.addUser = '{:,.0f}'.format(row['add_user_num'])
        entries.append(rd)
    if export:
        exportName = '作弊黑名单监测日表' + str(st)
        table_titles = [("dates", u"日期", dw_const.COLUMN_TYPE.STRING),
                        ("deviceNum", u"累计设备量", dw_const.COLUMN_TYPE.STRING),
                        ("addNum", u"新增设备量", dw_const.COLUMN_TYPE.STRING),
                        ("userNum", u"累计wax用户量", dw_const.COLUMN_TYPE.STRING),
                        ("addUser", u"新增wax用户量", dw_const.COLUMN_TYPE.STRING)]
        return dw_utils.ExportExcel(entries, table_titles, exportName)
    count_result = db.SQL_BI(count_sql)
    count = count_result[0]['count1'] if len(count_result) > 0 else 0
    params = dict()
    params['page'] = page
    params['pageCount'] = dw_utils.pageCount(int(count),
                                             dw_const.DEFAULT_PAGE_SIZE)
    params['count'] = count
    params['records'] = entries
    return dw_utils.toSuccessView(params)


@log.run_safe
def blacklist_types(_params):
    page = dw_utils.getDftValue(_params, 'page', 1)
    start = (int(page) - 1) * dw_const.DEFAULT_PAGE_SIZE
    export = dw_utils.getDftValue(_params, 'export', False)
    date = dw_utils.OutFormatDate(dw_utils.Yesterdays(1))
    st = dw_utils.getDftValue(_params, 'startDate', date)
    et = dw_utils.getDftValue(_params, 'endDate', date)
    searchName = dw_utils.getDftValue(_params, 'searchName', '-2')
    resourceID = dw_utils.getDftValue(_params, 'resourceID', "-2")
    st = st.replace("-", "")
    et = et.replace("-", "")
    argsSort = sql_utils.orderBySql(_params)

    sql = "select act_cate,dates,COALESCE(device_num,0) as device_num,COALESCE(add_device_num,0) as add_device_num,COALESCE(user_num,0) as user_num,COALESCE(add_user_num,0) as add_user_num  from ab_fake_device_cate_stat where dates>='{0}' AND dates<='{1}'".format(
        st, et)

    count_sql = "select count(1) as count1 from ab_fake_device_cate_stat where dates>='{0}' AND dates<='{1}'".format(
        st, et)

    if resourceID != '-2':
        a_sql = ' AND resource_id={0}'.format(resourceID)
        sql = sql + a_sql
        count_sql = count_sql + a_sql
    # 全部资源,等于空兼容历史数据
    else:
        a_sql = ' AND (resource_id=0 or resource_id= "")'
        sql = sql + a_sql
        count_sql = count_sql + a_sql

    if searchName != '-2':
        b_sql = " AND act_cate = '{0}'".format(searchName)
        sql += b_sql
        count_sql += b_sql
    sql = sql + " ORDER BY 1=1" + argsSort

    if not export:
        sql = "select * from({0})a".format(
            sql) + " limit %s,%s" % (start, dw_const.DEFAULT_PAGE_SIZE)
    entries = []
    # print sql
    rows = db.SQL_BI(sql)
    for row in rows:
        rd = dw_utils.Dict()
        rd.dates = row['dates']
        rd.actCate = dw_const.cheat_map_dict.get(row['act_cate'], '未知')
        rd.deviceNum = '{:,.0f}'.format(row['device_num'])
        rd.addNum = '{:,.0f}'.format(row['add_device_num'])
        rd.userNum = '{:,.0f}'.format(row['user_num'])
        rd.addUser = '{:,.0f}'.format(row['add_user_num'])
        entries.append(rd)
    if export:
        exportName = '作弊监测黑名单类型库监测日表' + str(st)
        table_titles = [("dates", u"日期", dw_const.COLUMN_TYPE.STRING),
                        ("actCate", u"异常类型", dw_const.COLUMN_TYPE.STRING),
                        ("deviceNum", u"累计设备量", dw_const.COLUMN_TYPE.STRING),
                        ("addNum", u"新增设备量", dw_const.COLUMN_TYPE.STRING),
                        ("userNum", u"累计wax用户量", dw_const.COLUMN_TYPE.STRING),
                        ("addUser", u"新增wax用户量", dw_const.COLUMN_TYPE.STRING)]
        return dw_utils.ExportExcel(entries, table_titles, exportName)
    count_result = db.SQL_BI(count_sql)
    count = count_result[0]['count1'] if len(count_result) > 0 else 0
    params = dict()
    params['page'] = page
    params['pageCount'] = dw_utils.pageCount(int(count),
                                             dw_const.DEFAULT_PAGE_SIZE)
    params['count'] = count
    params['records'] = entries
    return dw_utils.toSuccessView(params)
