# coding:utf-8
from app import create_app, celery_app
import platform
node_name = platform.node()
app = create_app(node_name or 'default')
app.app_context().push()
