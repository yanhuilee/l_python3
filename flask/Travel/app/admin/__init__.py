# _*_ coding:utf-8 _*_

from flask import Blueprint

admin = Blueprint("admin", __name__)

import app.admin.views
import app.admin.scenic_views
import app.admin.area_views
import app.admin.travels_views
import app.admin.user_views
