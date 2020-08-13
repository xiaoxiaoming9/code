# coding:utf-8
from . import week_report as app, week_views, login_required
from app.utils import dw_utils, dw_const
from flask import request


#周平台数据
@app.route('/week_report/platform_bi.do', methods=['GET'])
@login_required
def platform_bi():
    """
    @api {get} /week_report/platform_bi.do 获取周报表平台数据
    @apiGroup week_report
    @apiName platform_bi
    @apiVersion 2.0.0
    @apiParam dateDay: 2019-09-08
    @apiDescription 返回指定日期开始，7天的数据汇总
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
    {    
        "message": "", 
        "code": 200, 
        "data": 
        { 
            "count": 4, 
            "records":
            [ 
                {   
                    "platformName": "微博", 
                    "platformId": 1, 
                    "reqNum" : 1234,                --竞价请求量
                    "balance": 1000000,             --预算(分)
                    "expNum" : 1234,                --竞价请求量
                    "customNum" : 34,               --客户数
                    "expSum" : 1234,                --消耗量(分)
                    "balanceRate": 0,               --预算使用率(单位%0.01)
                    "fillRate": 0,                  --流量填充率(单位%0.01)
                    "cpm" : 1234,                   --(分)　llok 
                    "cpc" : 1234,                   --(分)
                    "actNum" : 14,                  --激活量
                },
                ...
            ], 
        } 
    }
    """
    return week_views.platform_bi(request.args)


# 周消耗分布
@app.route('/week_report/consum_desc.do', methods=['GET'])
@login_required
def consum_desc():
    """
    @api {get} /week_report/consum_desc.do 获取周消耗分布
    @apiGroup week_report
    @apiName consum_desc
    @apiVersion 2.0.0
    @apiParam dateDay: 2019-09-08
    @apiParam type 0平台 1代理商 2行业 3营销云 4 oCPM
    @apiDescription 返回指定日期开始，7天的消耗分布占比
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
    {
        "message": "", 
        "code": 200, 
        "data": 
        { 
            "count": 4, 
            "records":
            [ 
                {
                   "name": "微博",     --名称
                   "rate": 9810           --消耗占比(单位%0.01)
               }, 
               {
                    "name": "头条",     --名称
                   "rate": 50           --消耗占比(单位%0.01)
                },
                ...
            ], 
        } 
    }
    """
    return week_views.consum_desc(request.args)


#周消耗走势
@app.route('/week_report/sum_trend.do', methods=['GET'])
@login_required
def sum_trend():
    """
    @api {get} /week_report/sum_trend.do 周消耗走势
    @apiGroup week_report
    @apiName sum_trend
    @apiVersion 2.0.0
    @apiParam dateDay: 2019-09-07
    @apiParam platformID 默认请求全部平台id,没有的数据库不会存储数据
    platformId: [0,1,3,8,12,5004,5001,5002,10,13,11002,11003,11004,11005,11006,9,7,5003,11,4,6,2,5]
    @apiDescription 返回指定日期开始，7天消耗走势

    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
        {
            "message": "",
            "code": 200,
            "data": {
                "count": 14,　　　　　　-- 总条数
                "records": [{         --总数据列表
                    "11003": {         -- 平台id
                        "sort_id": 11,  --排序ｉｄ
                        "data": [{      -- 该平台下的数据
                            "date": "20190901",　-- 日期
                            "sum": "0.00",      -- 消耗
                            "rate": "0%"        -- 环比增长
                        }, {
                            "date": "20190902",
                            "sum": "0.00",
                            "rate": "0%"
                        }],
                        "id": "11003",　　　--平台ｉｄ
                        "title": "格调"     -- 平台名字
                    },
                    "11": {
                        "sort_id": 18,
                        "data": [{
                            "date": "20190901",
                            "sum": "0.00",
                            "rate": "0%"
                        }],
                        "id": "11",
                        "title": "小敦圈"
                    }
                }]
            }
        }
    """
    return week_views.sum_trend(request.args)


# 营销云数据
@app.route('/week_report/cloud_bi.do', methods=['GET'])
@login_required
def cloud_bi():
    """
    @api {get} /week_report/cloud_bi.do 营销云数据
    @apiGroup week_report
    @apiName cloud_bi
    @apiVersion 2.0.0
    @apiParam dateDay: 2019-09-07
    @apiDescription 返回指定日期开始，7天的数据汇总
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
        {
            "message": "",
            "code": 200,
            "data": {
                "count": 11,
                "records": [{
                    "cpm": "12.05",
                    "cloudName": "武汉微思敦网络技术有限公司",
                    "balanceRate": "107.48%",
                    "cpc": "192.45",
                    "saasId": 7000001,
                    "expSumTotal": "320,580.67",
                    "expSum": "319,565.07",
                    "customNum": 41,
                    "balance": "297,320",
                    "platformName": "微博"
                }]
            }
        }
    """
    return week_views.cloud_bi(request.args)


# 周代理商数据
@app.route('/week_report/channel_bi.do', methods=['GET'])
@login_required
def channel_bi():
    """
    @api {get} /week_report/channel_bi.do 获取周代理商数据
    @apiGroup week_report
    @apiName channel_bi
    @apiVersion 2.0.0
    @apiParam dateDay: 2019-09-07
    @apiDescription 返回指定日期开始，7天的数据汇总
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
    {
        "message": "", 
        "code": 200, 
        "data": 
       { 
            "count": 4, 
            "records":
            [ 
                {
                    "channelName": "第一事业部", 
                    "channelId": 1,    
                    "platformName": "微博", 
                    "platformId": 1, 
                    "balance": 1000000,             --预算(分)
                    "customNum" : 34,               --客户数
                    "expSum" : 1234,                --消耗量(分)
                    "balanceRate": 0,               --预算使用率(单位%0.01)
                    "cpm" : 1234,                   --(分)
                    "cpc" : 1234,                   --(分)
                    "actNum" : 14,                  --激活量
                },
                ...
            ], 
        } 
    }
    """
    return week_views.channel_bi(request.args)


# 周消耗top10
@app.route('/week_report/custom_top_10.do', methods=['GET'])
@login_required
def custom_top_10():
    """
    @api {get} /week_report/custom_top_10.do 获取消耗top10
    @apiGroup week_report
    @apiName custom_top_10
    @apiVersion 2.0.0
    @apiParam dateDay: 2019-09-07
    @apiDescription 返回指定日期开始，7天的数据汇总

    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
    {
        "message": "", 
        "code": 200, 
        "data": 
        { 
            "count": 4, 
            "records":
            [ 
                {   
                    "platformName": "微博", 
                    "platformId": 1, 
                    "custommName": "微博", 
                    "customId": 1, 
                    "balance": 1000000,             --预算(分)
                    "expSum" : 1234,                --消耗量(分)
                    "cpm" : 1234,                   --(分)　llok 
                    "cpc" : 1234,                   --(分)
                    "cpa" : 1234,                   --(分)
                },
                ...
            ], 
        } 
    }
    """
    return week_views.custom_top_10(request.args)


# ocpm数据
@app.route('/week_report/ocpm_trend.do', methods=['GET'])
@login_required
def ocpm_consume_trend():
    """
    @api {get} /week_report/ocpm_trend.do 获取ocpm数据
    @apiGroup week_report
    @apiName ocpm_consume_trend
    @apiVersion 2.0.0
    @apiParam dateDay: 2019-10-15
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
    {
        "message": "",
        "code": 200,
        "data": {
            "count": 6,
            "records": [{
                "semen": "表单提交",                       种子数据
                "productName": "中信银行信用卡",            产品
                "businessName": "金融-银行/银行产品",       行业
                "expSum": "1,296,669.99",                消耗
                "channelName": "营销部",                  代理商
                "platformName": "微博"                    资源
            }, {
                "semen": "激活",
                "productName": "克隆战争—IOS",
                "businessName": "游戏-APP-卡牌",
                "expSum": "13,031,259.98",
                "channelName": "营销部",
                "platformName": "微博"
            }]
        }
    }
    """
    return week_views.ocpm_consume_trend(request.args)


# 导出周报
@app.route("/week_report/export_bi.do", methods=['GET'])
@login_required
def export_bi():
    """
    @api {get} /week_report/export_bi.do 导出周报表
    @apiGroup week_report
    @apiName week_report_export_bi
    @apiVersion 2.0.0
    @apiParam dateDay: 2019-09-07
    @apiParam export: true
    @apiDescription 返回指定日期开始，7天的数据汇总
    """
    date = dw_utils.OutFormatDate(dw_utils.Yesterdays(1))
    date = dw_utils.getDftValue(request.args, 'dateDay', date)
    table = []
    table.append(
        (u'平台数据', week_views.platform_bi({
            "dateDay": date,
            "export": 1
        })))
    table.append((u'消耗分布--资源',
                  week_views.consum_desc({
                      "dateDay": date,
                      "export": 1,
                      "type": "0"
                  })))
    table.append((u'消耗分布--行业',
                  week_views.consum_desc({
                      "dateDay": date,
                      "export": 1,
                      "type": "2"
                  })))  #
    table.append((u'消耗分布--营销云',
                  week_views.consum_desc({
                      "dateDay": date,
                      "export": 1,
                      "type": "3"
                  })))
    table.append((u'消耗分布--代理商',
                  week_views.consum_desc({
                      "dateDay": date,
                      "export": 1,
                      "type": "1"
                  })))
    table.append((u'oCPM产品消耗分布',
                  week_views.consum_desc({
                      "dateDay": date,
                      "export": 1,
                      "type": "4"
                  })))
    SUM_sort = dw_utils.week_views_sort.consume()
    for key, value in SUM_sort.items():
        data = week_views.sum_trend({
            "dateDay": date,
            "export": 1,
            "platformId": str(key)
        })
        platformName = dw_const.PID_NEW_NAMES[int(key)]
        if data[1] == [] or platformName is None:
            continue
        a = 0
        for i in data[1]:
            if i['sum'] != '0.00':
                a = 1
        if a == 0:
            continue
        if len(data[1]) != 7:
            data = (data[0], [])
        table.append((u'消耗走势--{0}'.format(platformName), data))
    table.append((u'营销云数据', week_views.cloud_bi({
        "dateDay": date,
        "export": 1
    })))
    table.append(
        (u'代理商数据', week_views.channel_bi({
            "dateDay": date,
            "export": 1
        })))
    table.append((u'客户数据（消耗前10）',
                  week_views.custom_top_10({
                      "dateDay": date,
                      "export": 1
                  })))
    table.append((u'oCPM数据',
                  week_views.ocpm_consume_trend({
                      "dateDay": date,
                      "export": 1
                  })))
    return dw_utils.ExportExcelSheets("周报[" + date + "]", table)
