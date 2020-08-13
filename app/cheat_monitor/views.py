# coding:utf-8
from . import cheat as app, monitor_views, login_required
from flask import request


@app.route('/cheat_monitor/hour.do', methods=['GET', 'POST'])
@login_required
def monitor_hour():
    if request.method == 'POST':
        datas = request.form
    else:
        datas = request.args
    """
    @api {GET，POST} /cheat_monitor/hour.do 流量过滤监测时表
    @apiGroup cheat_monitor
    @apiDescription 流量过滤监测时表
    @apiName monitor_hour
    @apiParam  resourceID 资源ｉｄ
    @apiParam  startDate   开始时间* 例子：2017-01-01
    @apiParam  endDate   结束时间* 例子：2017-01-01
    @apiParam  times   时间* 例子：times:1
    @apiParam  page 页数(从1开始)
    @apiParam　export: true　　　默认不传,导出按钮
    @apiParam  datesSort       日期(以下排序都为1是重小到大排序，2是从大到小排序，空值是默认排序)
    @apiParam  timesSort       '时间',
    @apiParam  reqUserSort     '过滤用户',
    @apiParam  reqCntSort      '过滤请求量'
    @apiParam  reqSumSort      '过滤广告位数量'
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
    {
        "message": "",
        "code": 200,
        "data": {
            "count": 9,
            "records": [{
                "dates": "20191120",
                "reqCnt": "1,636,187",
                "reqSum": "3,232,354",
                "times": "13",
                "platformName": "微博",
                "reqUser": "294,306"
            }, {
                "dates": "20191120",
                "reqCnt": "301",
                "reqSum": "301",
                "times": "13",
                "platformName": "爱豆",
                "reqUser": "131"
            }],
            "page": "1",
            "pageCount": 1
        }
    }
    """
    return monitor_views.monitor_hour(datas)


@app.route('/cheat_monitor/day.do', methods=['GET', 'POST'])
@login_required
def monitor_day():
    if request.method == 'POST':
        datas = request.form
    else:
        datas = request.args
    """
    @api {GET，POST} /cheat_monitor/day.do   流量过滤监测日表
    @apiGroup cheat_monitor
    @apiDescription 流量过滤监测日表
    @apiName monitor_day
    @apiParam  resourceID 资源ｉｄ
    @apiParam  startDate   开始时间* 例子：2017-01-01
    @apiParam  endDate   结束时间* 例子：2017-01-01
    @apiParam  page 页数(从1开始)
    @apiParam　export: true　　　默认不传,导出按钮
    @apiParam  datesSort       日期(以下排序都为1是重小到大排序，2是从大到小排序，空值是默认排序)
    @apiParam  reqUserSort     '过滤用户',
    @apiParam  reqCntSort      '过滤请求量'
    @apiParam  reqSumSort      '过滤广告位数量'
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
    {
        "message": "",
        "code": 200,
        "data": {
            "count": 11,
            "records": [{
                "dates": "20191119",
                "reqSum": "59,992,752",
                "platformName": "微博",
                "reqUser": "830,834",
                "reqCnt": "31,551,625"
            }, {
                "dates": "20191119",
                "reqSum": "425",
                "platformName": "小敦圈",
                "reqUser": "4",
                "reqCnt": "244"
            }],
            "page": "1",
            "pageCount": 2
        }
    }
    """
    return monitor_views.monitor_day(datas)


@app.route('/cheat_monitor/blacklist.do', methods=['GET', 'POST'])
@login_required
def blacklist_collect():
    if request.method == 'POST':
        datas = request.form
    else:
        datas = request.args
    """
    @api {GET，POST} /cheat_monitor/blacklist.do  作弊黑名单监测日表
    @apiGroup cheat_monitor
    @apiDescription 作弊黑名单监测日表
    @apiName blacklist_collect
    @apiParam  startDate   开始时间* 例子：2017-01-01
    @apiParam  endDate   结束时间* 例子：2017-01-01
    @apiParam  page 页数(从1开始)
    @apiParam　export: true　　　默认不传,导出按钮
    @apiParam  datesSort       　日期(以下排序都为1是重小到大排序，2是从大到小排序，空值是默认排序)
    @apiParam  deviceNumSort     累计设备码数量
    @apiParam  addDeviceNumSort  新增累计设备码数量
    @apiParam  userNumSort      　累计ｗａｘ用户量
    @apiParam  addUserNum      　　新增ｗａｘ用户量
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
    {
        "message": "",
        "code": 200,
        "data": {
            "count": 1,
            "records": [{
                "dates": "20191119",
                "addUser": "0",
                "userNum": "3,329,277",
                "addNum": "0",
                "deviceNum": "759,169"
            }],
            "page": "1",
            "pageCount": 1
        }
    }


    """
    return monitor_views.blacklist_collect(datas)


@app.route('/cheat_monitor/types.do', methods=['GET', 'POST'])
@login_required
def blacklist_types():
    if request.method == 'POST':
        datas = request.form
    else:
        datas = request.args
    """
    @api {GET，POST} /cheat_monitor/types.do 作弊监测黑名单类型库监测日表
    @apiGroup cheat_monitor
    @apiDescription 作弊监测黑名单类型库监测日表
    @apiName blacklist_types
    @apiParam  startDate   开始时间* 例子：2017-01-01
    @apiParam  endDate   结束时间* 例子：2017-01-01
    @apiParam  page 页数(从1开始)
    @apiParam  searchName  搜索栏,传递异常id到后端就行
    @apiParam　export: true　　　默认不传,导出按钮
    @apiParam  datesSort       　日期(以下排序都为1是重小到大排序，2是从大到小排序，空值是默认排序)
    @apiParam  deviceNumSort     累计设备码数量
    @apiParam  addDeviceNumSort  新增累计设备码数量
    @apiParam  userNumSort      　累计ｗａｘ用户量
    @apiParam  addUserNumSort     新增ｗａｘ用户量
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
    {
        "message": "",
        "code": 200,
        "data": {
            "count": 1,
            "records": [{
                "dates": "20191119",
                "addUser": "0",
                "userNum": "3,329,277",
                "actCate": "户机对应异常(1机n户/1户n机)",
                "addNum": "0",
                "deviceNum": "759,169"
            }],
            "page": "1",
            "pageCount": 1
        }
    }
    """
    return monitor_views.blacklist_types(datas)


# bid_req_filter_stat_day 流量过滤监测日表
# bid_req_filter_stat_hour　流量过滤监测时表
# ab_fake_device_stat　作弊黑名单监测日表
# ab_fake_device_cate_stat　作弊监测黑名单类型库监测日表
