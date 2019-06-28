# _*_ coding: utf-8 _*_

import os
from flask import render_template, request, flash, redirect, current_app, url_for
from werkzeug.utils import secure_filename
from . import admin
from app import db
from app.admin.forms import ScenicForm
from app.models import Scenic, Area
from app.admin.views import change_filename, addOplog, admin_login


@admin.route("/scenic/add", methods=["GET", "POST"])
# @admin_login
def scenic_add():
    """ 添加景区页面 """
    form = ScenicForm()
    # 为area_id添加属性
    # form.area_id.choices = [(v.id, v.name) for v in Area.query.all()]
    form.area_id.choices = [(1, "1")]
    if form.validate_on_submit():
        data = form.data
        # 判断景区是否存在
        scenic_count = Scenic.query.filter_by(title=data["title"]).count()
        # 判断是否有重复数据
        if scenic_count == 1:
            flash("景点已经存在", "err")
            return redirect(url_for("admin.scenic_add"))

        # 确保文件名
        file_logo = secure_filename(form.logo.data.filename)
        up_dir = current_app.config["UP_DIR"]
        if not os.path.exists(up_dir):
            # 创建多级目录
            os.makedirs(up_dir)
            os.chmod(up_dir, "rw")
        # 更改名称
        logo = change_filename(file_logo)
        # 保存文件
        form.logo.data.save(up_dir + logo)
        # 为Scenic类属性赋值
        scenic = Scenic(
            title=data["title"],
            logo=logo,
            star=int(data["star"]),
            address = data["address"],
            is_hot = int(data["is_hot"]),
            is_recommended = int(data["is_recommended"]),
            area_id = data["area_id"],
            introduction=data["introduction"],
            content=data["content"],
        )
        db.session.add(scenic)
        db.session.commit()
        addOplog("添加景区" + data["title"])
        flash("添加景区成功！", "ok")  # 使用flash保存添加成功信息
        return redirect(url_for("admin.scenic_add"))
    return render_template("admin/scenic_add.html", form=form)


@admin.route("/scenic/list/", methods=["GET"])
# @admin_login
def scenic_list():
    """
    景区列表页面
    """
    title = request.args.get('title', '', type=str)  # 获取查询标题
    page = request.args.get('page', 1, type=int)   # 获取page参数值
    # 根据标题搜索景区
    if title:
        page_data = Scenic.query.filter(Scenic.title.like("%" + title + "%")).order_by(
            Scenic.addtime.desc()                  # 根据添加时间降序
        ).paginate(page=page, per_page=5)          # 分页
    else:                                         # 显示全部景区
        page_data = Scenic.query.order_by(
            Scenic.addtime.desc()
        ).paginate(page=page, per_page=5)
    return render_template("admin/scenic_list.html", page_data=page_data)


@admin.route("/sceni/edit/<int:id>", methods=["GET", "POST"])
@admin_login
def scenic_edit(id=None):
    """
    编辑景区
    :param id:
    :return:
    """
    form = ScenicForm()
    form.area_id.choices = [(v.id, v.name) for v in Area.query.all()]
    form.submit.label.text = "修改"
    form.logo.validators = []
    scenic = Scenic.query.get_or_404(int(id))  # 根据ID查找景区
    # 获取所有景区信息
    if request.method == "GET":
        form.is_recommended.data = scenic.is_recommended
        form.is_hot.data = scenic.is_hot
        form.area_id.data = scenic.area_id
        form.star.data = scenic.star
        form.content.data = scenic.content
        form.introduction.data = scenic.introduction
    # 提交表单
    if form.validate_on_submit():
        data = form.data
        scenic_count = Scenic.query.filter_by(title=data["title"]).count()  # 判断标题是否重复
        # 判断是否有重复数据
        if scenic_count == 1 and scenic.title != data["title"]:
            flash("景点已经存在！", "err")
            return redirect(url_for('admin.scenic_edit', id=id))
        if not os.path.exists(current_app.config["UP_DIR"]):  # 判断目录是否存在
            os.makedirs(current_app.config["UP_DIR"])
            os.chmod(current_app.config["UP_DIR"], "rw")
        # 上传图片
        if form.logo.data != "":
            file_logo = secure_filename(form.logo.data.filename)           # 确保文件名安全
            scenic.logo = change_filename(file_logo)                       # 更改文件名
            form.logo.data.save(current_app.config["UP_DIR"] + scenic.logo)  # 保存文件

        # 属性赋值
        scenic.title = data["title"]
        scenic.address = data["address"]
        scenic.area_id = data["area_id"]
        scenic.star = int(data["star"])
        scenic.is_hot = int(data["is_hot"])
        scenic.is_recommended = int(data["is_recommended"])
        scenic.introduction = data["introduction"]
        scenic.content = data["content"]

        db.session.add(scenic)
        db.session.commit()    # 提交数据
        flash("修改景区成功！", "ok")
        return redirect(url_for('admin.scenic_edit', id=id))  # 跳转到编辑页面
    return render_template("admin/scenic_edit.html", form=form, scenic=scenic)


@admin.route("/scenic/del/<int:id>/", methods=["GET"])
@admin_login
def scenic_del(id=None):
    """
    景区删除
    """
    scenic = Scenic.query.get_or_404(id)  # 根据景区ID查找数据
    db.session.delete(scenic)             # 删除数据
    db.session.commit()
    flash("景区删除成功", "ok")           # 使用flash存储成功信息
    addOplog("删除景区"+scenic.title)  # 添加日志
    return redirect(url_for('admin.scenic_list', page=1))
