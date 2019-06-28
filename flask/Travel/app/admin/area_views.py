# _*_ coding: utf-8 _*_

from flask import render_template, request, flash, redirect, url_for
from . import admin
from app import db
from app.admin.forms import AreaForm
from app.models import Area
from app.admin.views import addOplog, admin_login


@admin.route('/area/add/',methods=["GET", "POST"])
@admin_login
def area_add():
    """
    添加地区
    """
    form = AreaForm()
    if form.validate_on_submit():
        data = form.data  # 接收数据
        area = Area.query.filter_by(name=data["name"]).count()
        # 说明已经有这个地区了
        if area == 1:
            flash("地区已存在", "err")
            return redirect(url_for("admin.area_add"))
        area = Area(
            name=data["name"],
            is_recommended=data['is_recommended'],
            introduction=data['introduction']
        )
        db.session.add(area)
        db.session.commit()
        addOplog("添加地区"+data["name"])  # 添加日志
        flash("地区添加成功", "ok")
        return redirect(url_for("admin.area_add"))
    return render_template("admin/area_add.html", form=form)


@admin.route("/area/list/", methods=["GET"])
@admin_login
def area_list():
    """
    标签列表
    """
    name = request.args.get('name', type=str)     # 获取name参数值
    page = request.args.get('page', 1, type=int)  # 获取page参数值
    if name:  # 搜索功能
        page_data = Area.query.filter_by(name=name).order_by(
            Area.addtime.desc()
        ).paginate(page=page, per_page=5)
    else:
        # 查找数据
        page_data = Area.query.order_by(
            Area.addtime.desc()
        ).paginate(page=page, per_page=5)
    return render_template("admin/area_list.html", page_data=page_data)


@admin.route("/area/edit/<int:id>", methods=["GET", "POST"])
@admin_login
def area_edit(id=None):
    """
    地区编辑
    """
    form = AreaForm()
    form.submit.label.text = "修改"
    area = Area.query.get_or_404(id)
    if request.method == "GET":
        form.name.data = area.name
        form.is_recommended.data = area.is_recommended
        form.introduction.data = area.introduction
    if form.validate_on_submit():
        data = form.data
        area_count = Area.query.filter_by(name=data["name"]).count()
        if area.name != data["name"] and area_count == 1:
            flash("地区已存在", "err")
            return redirect(url_for("admin.area_edit", id=area.id))
        area.name = data["name"]
        area.is_recommended = int(data["is_recommended"])
        area.introduction = data["introduction"]
        db.session.add(area)
        db.session.commit()
        flash("地区修改成功", "ok")
        return redirect(url_for("admin.area_edit", id=area.id))
    return render_template("admin/area_edit.html", form=form, area=area)


@admin.route("/area/del/<int:id>/", methods=["GET"])
@admin_login
def area_del(id=None):
    """
    标签删除
    """
    # filter_by在查不到或多个的时候并不会报错，get会报错。
    area = Area.query.filter_by(id=id).first_or_404()
    db.session.delete(area)
    db.session.commit()
    addOplog("删除地区"+area.name)  # 添加日志
    flash("地区<<{0}>>删除成功".format(area.name), "ok")
    return redirect(url_for("admin.area_list"))