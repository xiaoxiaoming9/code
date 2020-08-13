from flask import Blueprint
cheat = Blueprint('cheat', __name__)
from app.auth.views import login_required
from . import views