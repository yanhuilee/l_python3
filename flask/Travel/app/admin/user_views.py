# _*_ coding: utf-8 _*_

from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import or_
from . import admin
from app import db
from app.models import User
from app.admin.views import addOplog, admin_login


@admin.route("/user/list",  methods=["GET", "POST"])
@admin_login
def user_list():
    """
    会员列表
    :return:
    """
    page = request.args.get("page", 1, type=int)
    keyword = request.args.get("keyword", "", type=str)
    if keyword:
        # 根据姓名或者邮箱查询
        filters = or_(User.username == keyword, User.email == keyword)
        page_data = User.query.filter(filters).order_by(
            User.addtime.desc()
        ).paginate(page=page, per_page=5)
    else:
        page_data = User.query.order_by(
            User.addtime.desc()
        ).paginate(page=page, per_page=5)
    return render_template("admin/user_list.html", page_data=page_data)


@admin.route("/user/view/<int:id>/", methods=["GET"])
@admin_login
def user_view(id=None):
    """
    查看会员详情
    """
    from_page = request.args.get('fp')
    if not from_page:
        from_page = 1
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user, from_page=from_page)


@admin.route("/user/del/<int:id>/", methods=["GET"])
@admin_login
def user_del(id=None):
    """
    删除会员
    """
    page = request.args.get('page',1,type=int)
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    addOplog("删除会员"+user.name)  # 添加日志
    flash("删除会员成功！", "ok")
    return redirect(url_for('admin.user_list', page=page))

    # 意见建议列表
    page = request.args.get('page', 1, type=int) # 获取page参数值
    page_data = Suggestion.query.order_by(
        Suggestion.addtime.desc()
    ).paginate(page=page, per_page=5)
    return render_template("admin/suggestion_list.html", page_data=page_data)