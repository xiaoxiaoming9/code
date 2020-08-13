# coding:utf-8
from flask import Blueprint
week_report = Blueprint('week_report', __name__)
from app.auth.views import login_required
from . import views
