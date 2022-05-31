"""LqApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from article.urls import router as article_router
from books.urls import router as books_router

router = routers.DefaultRouter()  # 定义默认路由
router.registry.extend(article_router.registry)
router.registry.extend(books_router.registry)
# router.register(r'product', pviews.ArticleViewSet)  # 这里只注册了一个产品中心的路由


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^api/', include('article.urls'))
    # path(r'api/article', include('article.urls'))
]
