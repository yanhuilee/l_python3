"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.authentication import views
from rest_framework.documentation import include_docs_urls

import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from django.views.generic import TemplateView

from goods.view_base import GoodsListView
from goods.views import GoodsListViewSet


router = DefaultRouter()

# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name="goods")

urlpatterns = [
    path(r'admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path(r'^', router.urls),
    path(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),

    path(r'^xadmin/', xadmin.site.urls),
    path(r'^media/(P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 商品列表页
    path(r'goods/$', GoodsListView.as_view(), name="goods-list"),
    path(r'docs/', include_docs_urls(title="慕学生鲜")),

    # drf自带的token认证模式
    path(r'^api-token-auth/', views.obtain_auth_token),
]
