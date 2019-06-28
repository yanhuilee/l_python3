# _*_ coding: utf-8 _*_

from flask import render_template, request, flash, redirect, url_for
from . import admin
from app import db
from app.admin.forms import TravelsForm
from app.models import Travels, Scenic
from app.admin.views import addOplog, admin_login


@admin.route("/travels/add/", methods=["GET", "POST"])
@admin_login
def travels_add():
    """
    添加游记
    """
    form = TravelsForm()
    form.scenic_id.choices = [(v.id, v.title) for v in Scenic.query.all()]
    if form.validate_on_submit():
        data = form.data
        # 判断游记是否存在
        travels_count = Travels.query.filter_by(title=data["title"]).count()
        # 判断是否有重复数据。
        if travels_count == 1:
            flash("景点已经存在！", "err")
            return redirect(url_for('admin.travels_add'))
        travels = Travels(
            title=data["title"],
            author = data["author"],
            scenic_id = data["scenic_id"],
            content=data["content"],
        )
        db.session.add(travels)
        db.session.commit()
        addOplog("添加游记"+data["title"])  # 添加日志
        flash("添加游记成功！", "ok")
        return redirect(url_for('admin.travels_add'))
    return render_template("admin/travels_add.html", form=form)


@admin.route("/travels/list/", methods=["GET"])
@admin_login
def travels_list():
    """
    景区列表页面
    """
    keywords = request.args.get('keywords', '', type=str)
    page = request.args.get('page', 1, type=int)  # 获取page参数值
    if keywords :
        # 使用like实现模糊查询
        page_data = Travels.query.filter(Travels.title.like("%"+keywords+"%")).order_by(
            Travels.addtime.desc()
        ).paginate(page=page, per_page=5)
    else :
        page_data = Travels.query.order_by(
            Travels.addtime.desc()
        ).paginate(page=page, per_page=5)
    return render_template("admin/travels_list.html", page_data=page_data)


@admin.route("/travels/edit/<int:id>/", methods=["GET", "POST"])
@admin_login
def travels_edit(id=None):
    """
    编辑游记
    """
    form = TravelsForm()
    form.scenic_id.choices = [(v.id, v.title) for v in Scenic.query.all()]
    form.submit.label.text = "修改"
    travels = Travels.query.get_or_404(int(id))
    if request.method == "GET":
        form.scenic_id.data = travels.scenic_id
        form.content.data = travels.content
    if form.validate_on_submit():
        data = form.data
        travels_count = Travels.query.filter_by(title=data["title"]).count()
        # 判断是否有重复数据
        if travels_count == 1 and travels.title != data["title"]:
            flash("游记已经存在！", "err")
            return redirect(url_for('admin.travels_edit', id=id))

        travels.title = data["title"]
        travels.scenic_id = data["scenic_id"]
        travels.author = data["author"]
        travels.content = data["content"]

        db.session.add(travels)
        db.session.commit()
        flash("修改景区成功！", "ok")
        return redirect(url_for('admin.travels_edit', id=id))
    return render_template("admin/travels_edit.html", form=form, travels=travels)


@admin.route("/travels/del/<int:id>/", methods=["GET"])
@admin_login
def travels_del(id=None):
    """
    景区删除
    """
    travels = Travels.query.get_or_404(id)
    db.session.delete(travels)
    db.session.commit()
    flash("游记删除成功", "ok")
    addOplog("删除游记"+travels.title)  # 添加日志
    return redirect(url_for('admin.travels_list', page=1))