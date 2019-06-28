django rest framework + xadmin后台开发环境

#### 一、项目初始化
```py
pip install -i https://pypi.douban.com/simple django djangorestframework 
    markdown django-filter
    mysqlclient pillow(图片处理)

# 启动项目
django-admin startproject MxShop
python manage.py runserver 127.0.0.1:80
```

settings.py
```py
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# 指明数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxshop',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {'init_commnad': 'SET storage_engine=INNODB;'},
    }
}
```

#### 二、model 设计
```
python manage.py startapp app_name
    uses goods trade user_option(用户操作)
    

gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), 
    default="female", verbose_name="性别")
```

- migrations 表生成
```
make migrations # 生成修改记录
migrate [app_name]
```

- xadmin 后台管理系统的配置

```
install
    django-crispy-forms
    django-reversion
    django-formtools
    future
    httplib2
    six
    
    # excel
    xlwt xlsxwriter
```

```
INSTALLED_APPS = [
    'crispy_forms',
    'xadmin',
]
```

create superuser
url

- 导入商品类别数据
```
goods/images
db_tools/data/category product
```


urls.py

#### 三、商品列表页 view
- 1、goods/views_base.py

framework: auth
`django-guardian coreapi`

```
INSTALLED_APPS = [
    'rest_framework',
]

urlpatterns = 
```
- 2、django的serializer序列化model
- 3、apiview方式实现商品列表页: view.py

- 4、drf的modelserializer 商品列表页功能
- 5、GenericView 方式实现商品列表页和分页功能
```
Using mixins
Pagination
```
- 6、viewsets和router完成商品列表页
```
GenericViewSet(viewset)  --drf
GenericAPIView           --drf
APIView                  --drf
View                     --django

mixin
    CreateModelMixin
    ListModelMixin
    UpdateModelMixin
    RetrieveModelMixin
    DestoryModelMixin
```

- 7、drf的request和response
- 8、drf的过滤，搜索和排序

#### 四、商品类型
- 6-1 商品类- 别数据接口-1
- 6-3 vue展示商品分类数据
- 6-6 vue的商品搜索功能

#### 五、登录和注册
- 7-1 drf的token登录和原理

#### 六、商品模块
- 商品详情页
- 热卖商品接口
- 用户收藏接口
- drf 的权限验证

#### 七、用户中心模块
- 用户个人信息修改
- 用户留言功能
- 收货地址列表页

#### 八、购物车、订单管理和支付功能

#### 九、首页、商品数量、缓存、限速功能开发
- 轮播图
- 新品功能接口开发
- 首页商品分类显示
- 商品点击数、收藏数
- 商品库存和销量
- drf 缓存

#### 十、第三方登录