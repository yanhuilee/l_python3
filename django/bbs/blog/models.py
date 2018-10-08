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


class Category(models.Model):
    """ 文章分类 """
    nid = models.AutoField(primary_key=True)
    # 分类标题
    title = models.CharField(max_length=32)
    # 外键关联博客，一个博客站点可以有多个分类
    blog = models.ForeignKey(to="Blog", to_field="nid")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """ 标签 """
    nid = models.AutoField(primary_key=True)
    # 标签名
    title = models.CharField(max_length=32)
    # 所属博客
    blog = models.ForeignKey(to="Blog", to_field="nid")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "标签"
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


class ArticleDetail(models.Model):
    """ 文章详情表 """

    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article", to_field="nid")

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name


class ArticleToTag(models.Model):
    """ 文章和标签的多对多关系表 """

    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid")
    tag = models.ForeignKey(to="Tag", to_field="nid")

    def __str__(self):
        return "{}-{}".format(self.article.title, self.tag.title)

    class Meta:
        unique_together = (("article", "tag"),)
        verbose_name = "文章-标签"
        verbose_name_plural = verbose_name


class ArticleUpDown(models.Model):
    """ 点赞表 """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", null=True)
    article = models.ForeignKey(to="Article", null=True)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("article", "user"),)
        verbose_name = "文章点赞"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """ 评论表 """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid")
    user = models.ForeignKey(to="UserInfo", to_field="nid")
    content = models.CharField(max_length=255)  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True, blank=True)  # blank=True 在django admin里面可以不填

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name