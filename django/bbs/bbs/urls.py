"""bbs URL Configuration

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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.static import serve
from django.conf import settings

from blog import views
from blog import urls as blog_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),

    path('register/', views.register),

    path('^blog/', include(blog_urls)),

    path('^get_valid_img.png/', views.get_valid_img),
    # 极验滑动验证码 获取验证码的url
    path('pc-geetest/register', views.get_geetest),

    # 校验用户名是否已被注册
    path('^check_username_exist/$', views.check_username_exist),
    # media相关的路由设置
    path('^media/(P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT})
]
