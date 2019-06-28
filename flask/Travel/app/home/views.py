# _*_ coding:utf-8 _*_

from . import home
from app import db
from app.home.forms import LoginForm, RegisterForm, SuggestionForm
from app.models import User, Userlog, Area, Scenic, Suggestion, Collect, Travels
from flask import render_template, url_for, redirect, flash, session, request
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from functools import wraps
import json


def user_login(f):
    """ 登录装饰器 """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            # 判断用户没有登录，跳到登录页
            return redirect(url_for("home.login"))
        return f(*args, **kwargs)
    return decorated_function


@home.route("/login", methods=["GET", "POST"])
def login():
    """ 登录 """
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        # 判断用户名和密码是否匹配
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_pwd(data["pwd"]):
            flash("邮箱或密码错误！", "err")
            # 返回登录页
            return redirect(url_for("home.login"))
        session["user_id"] = user.id
        # 将用户登录信息写入Userlog表
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.index"))
    return render_template("home/login.html", form=form)


@home.route("/logout/")
def logout():
    """
    退出登录
    """
    # 重定向到home模块下的登录。
    session.pop("user_id", None)
    return redirect(url_for('home.login'))


@home.route("/")
def index():
    """ 首页 """
    area = Area.query.all()
    # 热闹区域
    hot_area = Area.query.filter_by(is_recommended=1).limit(2).all()
    scenic = Scenic.query.filter_by(is_hot=1).all()
    return render_template("home/index.html", area=area, hot_area=hot_area, scenic=scenic)


@home.route("/register/", methods=["GET", "POST"])
def register():
    """ 注册功能 """
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        # 为 User类属性赋值
        user = User(
            username=data["username"],
            email=data["email"],
            # 密码加密
            pwd=generate_password_hash(data["pwd"]),
        )
        db.session.add(user)
        db.session.commit()
        # 使用 flask 存储成功信息
        flash("注册成功!", "ok")
    return render_template("home/register.html", form=form)


@home.route("/info/<int:id>")
def info(id=None):
    """ 详情页 """
    # 根据景区ID获取景区数据，如果不存在返回404
    scenic = Scenic.query.get_or_404(int(id))
    user_id = session.get("user_id", None)
    if user_id:
        count = Collect.query.filter_by(user_id=int(user_id), scenic_id=int(id)).count()
    else:
        # 用户未登录状态
        user_id = 0
        count = 0
    return render_template("/home/info.html", scenic=scenic, user_id=user_id, count=count)


@home.route("/travels/<int:id>/")
def travels(id=None):
    """ 详情页 """
    travels = Travels.query.get_or_404(int(id))
    return render_template("home/travels.html", travels=travels)


@home.route("/collect_add/")
@user_login
def collect_add():
    """ 收藏景区 """
    # 接收传递的参数scenic_id
    scenic_id = request.args.get("scenic_id", "")
    user_id = session["user_id"]
    # 根据用户ID和景区ID判断是否该收藏
    collect = Collect.query.filter_by(
        user_id=int(user_id),
        scenic_id=int(scenic_id)
    ).count()
    # 已收藏
    if collect == 1:
        data = dict(ok=0)
    # 未收藏进行收藏
    if collect == 0:
        collect = Collect(
            user_id=int(user_id),
            scenic_id=int(scenic_id)
        )
        data.session.add(collect)
        db.session.commit()
        data = dict(ok=1)

    # 返回json数据
    return json.dumps(data)


@home.route("/collect_list")
@user_login
def collect_list():
    page = request.args.get("page", 1, type=int)
    # 根据user_id删选Collect表数据
    page_data = Collect.query.filter_by(user_id=session["user_id"]).order_by(
        Collect.addtime.desc()
    ).paginate(page=page, per_page=3)
    return render_template("home/collect_list.html", page_data=page_data)


@home.route("/collect_cancel")
@user_login
def collect_cancel():
    """ 取消收藏景区 """
    id = request.args.get("id", "")
    # 获取当前用户ID
    user_id = session["user_id"]
    collect = Collect.query.filter_by(id=id, user_id=user_id).first()
    if collect:
        db.session.delete(collect)
        db.session.commit()
        data = dict(ok=1)
    else:
        data = dict(ok=-1)
    return json.dumps(data)


@home.route("/search")
def search():
    """ 搜索功能 """
    # 获取page参数值，默认为1
    page = request.args.get("page", 1, type=int)
    # 获取所有城市
    area = Area.query.all()
    # 地区
    area_id = request.args.get("area_id", type=int)
    # 星级
    star = request.args.get("star", type=int)

    if area_id or star:
        # 根据星级搜索景区
        filters = and_(Scenic.area_id == area_id, Scenic.star == star)
        page_data = Scenic.query.filter(filters).paginate(page=page, per_page=6)
    else:
        # 搜索全部景区
        page_data = Scenic.query.paginate(page=page, per_page=6)
    return render_template("home/search.html", page_data=page_data, area=area,
                           area_id=area_id, star=star)


@home.route("/about/")
def about():
    """
    关于我们
    """
    return render_template('home/about.html')


@home.route("/contact/", methods=["GET", "POST"])
def contact():
    """
    联系我们
    """
    form = SuggestionForm()  # 实例化SuggestionForm类
    # 判断用户是否提交表单
    if form.validate_on_submit():
        data = form.data  # 接收用户提交的表单数据
        # 为属性赋值
        suggestion = Suggestion(
            name=data["name"],
            email=data["email"],
            content=data["content"],
        )
        db.session.add(suggestion)  # 添加数据
        db.session.commit()
        flash("发送成功！", "ok")  # 用flask存储发送成功消息
        form.content.data = ''  # 设置内容为空
    return render_template('home/contact.html', form=form)  # 渲染模板，并传递表单数据
