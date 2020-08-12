# coding:utf-8
from flask import Flask
from conf.config import conf
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect  # 开启csrf验证
from celery import Celery

login_manager = LoginManager()
celery_app = Celery(__name__, broker=conf.CELERY_BROKER_URL)
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.idfas'])


def create_app(node_name):
    app = Flask(__name__)
    app.debug = conf.DEBUG
    app.config.from_object(conf)
    login_manager.setup_app(app)
    celery_app.conf.update(app.config)
    CSRFProtect(app)

    @app.after_request
    def after_request(response):
        from flask_wtf.csrf import generate_csrf
        csrf_token = generate_csrf()
        response.set_cookie('csrf_token', csrf_token)
        return response
    from info.utils.commons import do_rank_class, do_news_status
    app.add_template_filter(do_rank_class, 'rank_class')
    app.add_template_filter(do_news_status, 'news_status')
    from info.utils.commons import login_user_data

    @app.errorhandler(404)
    @login_user_data
    def handle_page_not_found(e):
        user = g.user
        return render_template('news/404.html', user=user)
    app.secret_key = '2ze3j543bsps36tq0o'  # Change this!
    login_manager.init_app(app)
    # 声明默认视图函数为login，当我们进行@require_login时，如果没登陆会自动跳到该视图函数处理
    login_manager.login_view = "req"
    # 可设置为None，basic，strong已提供不同的安全等级
    login_manager.session_protection = 'strong'
    # 下面的是注册蓝本 和引入蓝本
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .realtime_win import realtime_win as bid_win_blueprint
    from .nginx_analysis import nginx_analysis as nginx_analysis_blueprint
    # from .realtime import realtime as realtime_blueprint
    from .reports import reports as reports_blueprint
    from .reports.operating import operating as operating_blueprint
    from .reports.realtime import realtime as realtime_blueprint
    from .reports.daily_report import daily as daily_blueprint
    from .reports.interval_report import interval as interval_blueprint
    from .reports.cumulative_repoert import cumulative as cumulative_blueprint
    from .reports.function_report import function as function_blueprint
    # from .operating import operating as operating_blueprint
    from .portraits import portraits as portraits_blueprint
    from .reports.week_report import week_report as week_report
    from .reports.user_portrayal import portrayal as portrayal_blueprint
    from .reports.cheat_monitor import cheat as cheat_blueprint
    # from .utils import utils as utils_blueprint
    from .data_toolbar.data_manager import datas as datas_blueprint
    from .data_toolbar.data_export import package as package_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(function_blueprint)
    app.register_blueprint(cumulative_blueprint)
    app.register_blueprint(interval_blueprint)
    app.register_blueprint(daily_blueprint)
    app.register_blueprint(auth_blueprint)  # , url_prefix="/auth")
    app.register_blueprint(bid_win_blueprint)
    app.register_blueprint(nginx_analysis_blueprint)
    app.register_blueprint(realtime_blueprint)
    app.register_blueprint(reports_blueprint)
    app.register_blueprint(operating_blueprint)
    app.register_blueprint(portraits_blueprint)
    app.register_blueprint(week_report)
    app.register_blueprint(datas_blueprint)
    app.register_blueprint(package_blueprint)
    app.register_blueprint(portrayal_blueprint)
    app.register_blueprint(cheat_blueprint)
    return app
