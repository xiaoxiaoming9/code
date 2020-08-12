# coding:utf-8
from flask import Blueprint
main = Blueprint('main', __name__)
from ..auth.views import login_required
from . import error_views, views
