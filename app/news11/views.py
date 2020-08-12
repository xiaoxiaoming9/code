from . import passport_blu
from flask import request, abort, jsonify
from info.utils.response_code import RET  # 导入utils下面的response模块
from info.utils.captcha.captcha import captcha
from flask import current_app
from info import constants
from info import redis_store
from flask import make_response
import re
import random
from info.libs.yuntongxun.sms import CCP
from info.models import User, db
from flask import session


# 发送短信验证码
@passport_blu.route('/sms_code', methods=['POST'])
def send_sms_code():
    req_dict = request.json
    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    mobile = req_dict.get('mobile')
    # 得到验证码
    image_code = req_dict.get('image_code')
    # 得到图片标识
    image_code_id = req_dict.get('image_code_id')
    print(image_code_id)
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 对手机好进行判断
    if not re.match(r'^1[3-9]\d{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号有误')


    try:
        real_image_code = redis_store.get('image_code_id:%s' % image_code_id)  # 下面这样设置的,取一样
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取图片验证码失败')

    # 判断图片验证码有无过期   ? 上面判断了这里为什么还要判断
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmas='图片已经过期了')


    if real_image_code != image_code:
        return jsonify(errno=RET.NODATA, errmsg='图片验证码错误')

    sms_code = '%06d' % random.randint(0, 999999)
    current_app.logger.info('短信验证码为:%s' % sms_code)

    try:
        redis_store.set('sms_code:%s' % mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)

    except Exception as a:
        current_app.logger.error(a)
        return jsonify(errno=RET.DBERR, errmsg='保存短信验证码失败')
    res = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES / 60], 1)
    if res != 0:
        return jsonify(errno=RET.THIRDERR, errmsg='发送短信失败3333')

    return jsonify(errno=RET.OK, errmsg='发送短信成功')


# 这是图片验证码区域路由
@passport_blu.route('/image_code')
def get_image_code():
    """
    产生图片验证码:

    """
    image_code_id = request.args.get('image_code_id')
    if not image_code_id:
        # abort(400)
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    name, text, content = captcha.generate_captcha()
    current_app.logger.info('图片验证码为:%s' % text)

    try:
        redis_store.set('image_code_id:%s' % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存图片验证码失败')

    # 返回图片验证码
    response = make_response(content)
    print(content)
    print(response)
    # 设置在相应头中进行返回
    response.headers['Content_Type'] = 'image/jpg'
    return response

