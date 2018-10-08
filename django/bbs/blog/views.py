# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.http import JsonResponse
from geetest import GeetestLib
import logging
from blog import forms, models
from django.db.models import Count

# import sys  # utf-8
# reload(sys)
# sys.setdefaultencoding("utf-8")

# 生成一个logger实例，专门用来记录日志
logger = logging.getLogger(__name__)


def index(request):
    article_list = models.Article.objects.all()
    return render(request, "index.html", {"article_list": article_list})


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


def login(request):
    """使用极验滑动验证码的登录"""
    # if request.is_ajax()
    if request.method == "POST":
        # 初始化一个给ajax返回的数据
        result = {"status": 0, "msg": ""}

        username = request.POST.get("username")
        passward = request.POST.get("passward")

        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]

        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确，用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, passward=passward)
            if user:
                auth.login(request, user)
                result["msg"] = "/index"
            else:
                result["status"] = 1
                result["msg"] = "用户名或密码错误！"
        else:
            result["status"] = 1
            result["msg"] = "验证码错误！"

        return JsonResponse(result)
    return render(request, "login2.html")


def logout(request):
    """ 注销 """
    auth.logout(request)
    return redirect("/index/")


def get_geetest(request):
    """ 处理极验 获取验证码的视图 """
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def register(request):
    """注册"""
    if request.method == "POST":
        result = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)

        # 校验
        if form_obj.is_valid():
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            result["msg"] = "/index/"
        else:
            print(form_obj.errors)
            result["status"] = 1
            result["msg"] = form_obj.errors
        return JsonResponse(result)

    # 生成form对象
    form_obj = forms.RegForm()
    # print("".join(form_obj))
    return render(request, "register.html", {"form_obj": form_obj})


def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已被注册!"
    return JsonResponse(ret)


def home(request, username, *args):
    """ 个人博客主页 """
    logger.debug("home视图获取到用户名:{}".format(username))
    # 取用户对象
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        logger.warn("没有页面了...")
        return HttpResponse("404")
    # 用户文章
    blog = user.blog
    if not args:
        logger.debug("args没有接收到参数，默认走的是用户的个人博客页面！")
        # 文章列表
        article_list = models.Article.objejects.filter(user=user)
    else:
        if args[0] == "category":
            article_list = models.Article.objects.filter(user=user).filter(category_title=args[1])
        elif args[0] == "tag":
            article_list = models.Article.objects.filter(user=user).filter(tags__title=args[1])
        else:
            try:
                # 按照日期归档
                year, month = args[1].split("-")
                logger.debug("分割得到参数year:{}, month:{}".format(year, month))
                article_list = models.Article.objects.filter(user=user).filter(
                    create_time_year=year, create_time_month=month
                )
            except Exception as e:
                logger.warning("请求访问的日期归档格式不正确！！！")
                logger.warning((str(e)))
                return HttpResponse("404")
    return render(request, "home.html", {
        "username": username,
        "blog": blog,
        "article_list": article_list,
    })


def get_left_menu(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    # 按日期归档
    archive_list = models.Article.objects.filter(user=user).extra(
        select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")

    return category_list, tag_list, archive_list


def article_detail(request, username, pk):
    """
    :param username: 被访问的blog的用户名
    :param pk: 访问的文章的主键id值
    :return:
    """
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    # 找到当前的文章
    article_obj = models.Article.objects.filter(pk=pk).first()


    return render(
        request,
        "article_detail.html",
        {
            "username": username,
            "article": article_obj,
            "blog": blog,
        }
    )


import json
from django.db.models import F

def up_down(request):
    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get('is_up'))
    user = request.user
    response = {"state": True}
    try:
        models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
        models.Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
    except Exception as e:
        response["state"] = False
        response["first_action"] = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up

    return JsonResponse(response)