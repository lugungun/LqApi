from rest_framework import serializers

from article.models import Article, Category, Tag
from user_info.serializer import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    """分类的序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """标签的序列化器"""
    # 不允许重复的，所以需要覆写创建和更新方法
    def check_tag_obj_exists(self,validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag with text {} exists.'.format(text))

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super(TagSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super(TagSerializer, self).update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'


class ArticleCategorySerializer(serializers.ModelSerializer):
    """给分类详情的嵌套序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = ['url',
                  'title']

class CategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情序列化器"""
    articles = ArticleCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id',
                  'title',
                  'created',
                  'articles']


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    """博文序列化器"""

    # 作者参数设置为只读
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    # 用于创建/更新category外键，自动链接
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )

    # 字段验证
    def validated_category_id(self, value):
        if not Category.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError("category with id {} not exists!".format(value))
        return value

    # 方法覆写，如果输入的标签不寻在就创建
    def to_internal_value(self, data):  # 该方法愿作用是将请求中的原始json数据转化为python表现形式，还会对字段有效性做初步检查
        tags_data = data.get('tags')
        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)
        return super(ArticleSerializer, self).to_internal_value()

    class Meta:
        model = Article
        fields = '__all__'


class ArticleSerializer(ArticleBaseSerializer):
    """博文序列化器"""

    class Meta:
        model = Article
        fields = '__all__'
        # 仅可写但不展示
        extra_kwargs = {'body': {'write_only': True}}

class ArticleDetailSerializer(ArticleBaseSerializer):
    """博文详情序列化器"""

    # 渲染后的正文
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()
    # body_html字段，它会自动去调用get_body_html()方法，并将其返回结果作为需要序列化的数据
    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'



# class ArticleListSerializer(serializers.ModelSerializer):
#     # 作者参数设置为只读
#     author = UserSerializer(read_only=True)
#     # 添加文章超链接
#     url = serializers.HyperlinkedIdentityField(view_name='detail')
#
#     class Meta:
#         model = Article
#         fields = [
#             'url',
#             'author',
#             'title',
#             'body',
#             'created',
#             'updated'
#         ]
#
#
# class ArticleDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'
