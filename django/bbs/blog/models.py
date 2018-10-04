from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """ 用户信息表 """
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.png",
                              verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True)

    blog = models.OneToOneField(
        to="Blog", to_field="nid", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username

    class Meta(object):
        """类信息，用于admin管理"""
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Blog(models.Model):
    """博客信息"""
    nid = models.AutoField(primary_key=True)
    # 标题
    title = models.CharField(max_length=64)
    # 博客后缀
    site = models.CharField(max_length=32, unique=True)
    # 主题
    theme = models.CharField(max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "blog站点"
        verbose_name_plural = verbose_name


class Article(models.Model):
    """ 文章 """
    nid = models.AutoField(primary_key=True)
    # 文章标题
    title = models.CharField(max_length=50, verbose_name="文章标题")
    # 文章描述
    desc = models.CharField(max_length=255)
    # 创建时间  --> datetime()
    create_time = models.DateTimeField()

    # 评论数
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # 点赞数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)
    # 踩
    down_count = models.IntegerField(verbose_name="踩数", default=0)

    category = models.ForeignKey(to="Category", to_field="nid", null=True)
    user = models.ForeignKey(to="UserInfo", to_field="nid")
    tags = models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields={"article", "tag"},
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name


