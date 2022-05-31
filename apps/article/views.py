from django.shortcuts import render


# Create your views here.
from article.permissions import IsAdminUserOrReadOnly
from rest_framework import generics, viewsets, filters

from article.models import Article, Category, Tag
from article.serializer import ArticleSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, ArticleDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer




class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


