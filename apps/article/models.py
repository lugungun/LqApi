from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markdown import Markdown

# Create your models here.
class Category(models.Model):
    """
    文章分类
    """
    title = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        """
        把一个类的实例转成str输出
        :return:
        """
        return self.title


class Tag(models.Model):
    """标签"""
    text = models.CharField(max_length=20)

    # 定义模型元数据 是“任何不是字段的数据”
    class Meta:
        ordering = [-id]

        def __str__(self):
            return self.text


class Article(models.Model):
    """博文"""
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='articles') #关连数据删除，该外键置空
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='articles') #关连数据删除，该外键也删除
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    body = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        # toc是渲染后的目录
        return md_body, md.toc

    class Meta:
        ordering = ['-created']


