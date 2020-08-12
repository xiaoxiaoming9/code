# coding:utf-8
from flask import render_template, request
from . import main as app, login_required, common_views
from ..utils import dw_utils



@app.route('/list_platform_wead.do', methods=['GET', 'POST'])
@login_required
def list_platform_wead():
    """
    @api {GET,POST} list_platform_wead.do 数据中心资源筛选框获取路由
    @apiGroup main
    @apiDescription 数据中心资源筛选框获取路由
    @apiName realtime_request
    @apiUse SuccessBase
    @apiSuccessExample {json} 成功返回：
        {
            "message": "",
            "code": 200,
            "data": {
                "count": 16,
                "records": [{
                    "id": 1,
                    "name": "微博"
                }, {
                    "id": 12,
                    "name": "知乎"
                }{
                    "childen": [{
                        "id": 10,
                        "name": "最右"
                    }, {
                        "id": 3,
                        "name": "今日头条"
                    }],
                    "id": 100,
                    "name": "其它"
                }]
            }
        }
    """
    return common_views.listPlatformWeAD(request.args)
