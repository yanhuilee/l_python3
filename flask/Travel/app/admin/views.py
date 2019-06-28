# _*_ coding:utf-8 _*_

import os
import uuid
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, current_app, make_response
from functools import wraps
from . import admin
from app.admin.forms import LoginForm, PwdForm
from app.models import Oplog, Admin, User, Suggestion, Adminlog, Userlog
from app import db


def admin_login(f):
    """ 登录装饰器 """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def gen_rnd_filename():
    return datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex)


def change_filename(filename):
    """
    修改文件名称
    """
    fileinfo = os.path.splitext(filename)
    filename =  gen_rnd_filename() + fileinfo[-1]
    return filename


def addOplog(reason):
    """
    添加日志
    :param reason:
    :return:
    """
    oplog = Oplog(
        admin_id=session["admin_id"],
        ip=request.remote_addr,
        reason=reason
    )
    db.session.add(oplog)
    db.session.commit()


@admin.route("/")
@admin_login
def index():
    return render_template("admin/index.html")


@admin.route("/login", methods=["GET", "POST"])
def login():
    """登录"""
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        # 密码错误时，check_pwd返回false,则此时not check_pwd(data["pwd"])为真。
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误!", "err")
            return redirect(url_for("admin.login"))  # 跳转到后台登录页
        # 如果是正确的，就要定义session的会话进行保存。
        session["admin"] = data["account"]  # 存入session
        session["admin_id"] = admin.id  # 存入session
        # 创建数据
        adminlog = Adminlog(
            admin_id=admin.id,
            ip=request.remote_addr,
        )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(url_for("admin.index"))
    return render_template("admin/login.html",form=form)


@admin.route('/logout/')
@admin_login
def logout():
    """
    后台注销登录
    """
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))


@admin.route('/pwd/', methods=["GET", "POST"])
@admin_login
def pwd():
    """
    后台密码修改
    """
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for('admin.logout'))
    return render_template("admin/pwd.html", form=form)


@admin.route("suggestion_list/list", methods=["GET"])
@admin_login
def suggestion_list():
    """
    意见建议列表
    :return:
    """
    page = request.args.get('page', 1, type=int) # 获取page参数值
    page_data = Suggestion.query.order_by(
        Suggestion.addtime.desc()
    ).paginate(page=page, per_page=5)
    return render_template("admin/suggestion_list.html", page_data=page_data)


@admin.route("/suggestion/del/<int:id>/", methods=["GET"])
@admin_login
def suggestion_del(id=None):
    """
    删除意见
    """
    page = request.args.get('page', 1, type=int)
    suggestion = Suggestion.query.get_or_404(int(id))
    db.session.delete(suggestion)
    db.session.commit()
    addOplog("删除意见建议")  # 添加日志
    flash("删除成功！", "ok")
    return redirect(url_for('admin.suggestion_list', page=page))


@admin.route("/oplog/list/", methods=["GET"])
@admin_login
def oplog_list():
    """
    操作日志管理
    """
    page = request.args.get('page', 1, type=int) # 获取page参数值
    page_data = Oplog.query.join(
        Admin
    ).filter(
        Admin.id == Oplog.admin_id,
        ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/oplog_list.html", page_data=page_data)


@admin.route("/adminloginlog/list/", methods=["GET"])
@admin_login
def adminloginlog_list(page=None):
    """
    管理员登录日志
    """
    page = request.args.get('page', 1, type=int)  # 获取page参数值
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.admin_id,
        ).order_by(
        Adminlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/adminloginlog_list.html", page_data=page_data)


@admin.route("/userloginlog/list/", methods=["GET"])
@admin_login
def userloginlog_list(page=None):
    """
    会员登录日志列表
    """
    page = request.args.get('page', 1, type=int)  # 获取page参数值
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == Userlog.user_id,
        ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=5)
    return render_template("admin/userloginlog_list.html", page_data=page_data)


@admin.route('/ckupload/', methods=['POST', 'OPTIONS'])
@admin_login
def ckupload():
    """CKEditor 文件上传"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)

        filepath = os.path.join(current_app.static_folder, 'uploads/ckeditor', rnd_name)
        print(filepath)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('uploads/ckeditor', rnd_name))
    else:
        error = 'post error'

    res = """<script type="text/javascript">
        window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
        </script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response
