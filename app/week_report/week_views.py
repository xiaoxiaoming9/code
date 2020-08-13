# coding:utf8
from app.utils import dw_const, dw_utils, db_conn as db, log
import pymysql
from datetime import datetime as ddatetime, timedelta
import locale
locale.setlocale(locale.LC_ALL, '')
ESCP = pymysql.escape_string


@log.run_safe
def platform_bi(_params):
    date = dw_utils.getDftValue(_params, 'dateDay',
                                dw_utils.OutFormatDate(dw_utils.Yesterdays(1)))
    date = date.replace("-", "")
    export = dw_utils.getDftValue(_params, 'export', False)
    sql = "select * from tdw_week_platform where c_date = '{0}' and c_sum != 0 order by c_platform_id".format(
        ESCP(date))
    entries = []
    rows = db.SQL_DW(sql)
    sort_dict = dw_utils.week_views_sort.platform()
    for row in rows:
        rd = dw_utils.Dict()
        rd.platformId = row['c_platform_id']
        platformName = dw_const.PID_NEW_NAMES[int(row['c_platform_id'])]
        if platformName is None:  # 有新平台增加进行全局变量修改
            continue
        rd.platformName = platformName
        rd.reqNum = locale.format('%d', row['c_bid_cnt'], 1)
        rd.balance = locale.format('%d', row['c_balance'] / 100.00, 1)
        rd.expNum = locale.format('%d', row['c_exposure_cnt'], 1)
        rd.customNum = locale.format('%d', row['c_custom_cnt'], 1)
        rd.expSum = '{:,.2f}'.format(row['c_sum'] /
                                     100.00) if row['c_sum'] else 0
        if row['c_balance']:
            rd.balanceRate = '%s%%' % format(
                float(row['c_sum'] * 100.00) / float(row['c_balance']), '.2f')
        else:
            rd.balanceRate = '-'
        if row['c_bid_cnt'] and row['c_exposure_cnt']:
            rd.fillRate = '%s%%' % format(float(row['c_fill_rate'] / 100.00),
                                          '.2f')
        else:
            rd.fillRate = '-'
        rd.cpm = (format(
            float(row['c_sum'] * 10) / float(row['c_exposure_cnt']),
            '.2f')) if row['c_cpm'] != -1 else '-'
        if row['c_cpc'] > 0:
            rd.cpc = format((row['c_cpc'] / 100.00), '.2f')
        else:
            rd.cpc = '-'
        if int(row['c_platform_id']) == 0:
            rd.cpc = "-"
            rd.cpm = '-'
        rd.actNum = locale.format('%d', row['c_activate_cnt'], 1)
        entries.append(rd)
    entries_d = []
    for key, value in sort_dict.items():
        for row in entries:
            if value == int(row['platformId']):
                entries_d.append(row)

    if export:
        table_titles = [("platformName", u"资源", dw_const.COLUMN_TYPE.STRING),
                        ("reqNum", u"请求量", dw_const.COLUMN_TYPE.STRING),
                        ("balance", u"预算量", dw_const.COLUMN_TYPE.CENT),
                        ("expNum", u"曝光数量", dw_const.COLUMN_TYPE.STRING),
                        ("customNum", u"客户数", dw_const.COLUMN_TYPE.STRING),
                        ("expSum", u"消耗量", dw_const.COLUMN_TYPE.CENT),
                        ("balanceRate", u"预算使用率",
                         dw_const.COLUMN_TYPE.PERCENT),
                        ("fillRate", u"流量填充率", dw_const.COLUMN_TYPE.PERCENT),
                        ("cpm", u"CPM", dw_const.COLUMN_TYPE.CENT),
                        ("cpc", u"CPC", dw_const.COLUMN_TYPE.CENT),
                        ("actNum", u'激活数', dw_const.COLUMN_TYPE.STRING)]
        return (table_titles, entries_d)
    params = dict()
    params['count'] = len(entries_d)
    params['records'] = entries_d
    return dw_utils.toSuccessView(params)

