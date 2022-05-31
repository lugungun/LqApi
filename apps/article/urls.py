from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from article import views


router = DefaultRouter()
router.register(r'list', views.ArticleViewSet)
router.register(r'category', views.CategoryViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),

]