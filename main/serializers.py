from rest_framework import serializers
from .models import Requirement, FAQ, Contact, Tag, Publication, Paper, Review


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = ['id', 'title', 'description', 'file', 'image', 'tags', 'created_at', 'updated_at']

    def get_title(self, obj):
        request = self.context.get('request', None)
        lang = request.query_params.get('lang', 'en') if request else 'en'
        return getattr(obj, f'title_{lang}')

    def get_description(self, obj):
        request = self.context.get('request', None)
        lang = request.query_params.get('lang', 'en') if request else 'en'
        return getattr(obj, f'description_{lang}')


class PaperSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    keywords = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = '__all__'
        read_only_fields = ['author', 'views', 'date']

    def get_title(self, obj):
        request = self.context.get('request', None)
        lang = request.query_params.get('lang', 'en') if request else 'en'
        return getattr(obj, f'title_{lang}')

    def get_description(self, obj):
        request = self.context.get('request', None)
        lang = request.query_params.get('lang', 'en') if request else 'en'
        return getattr(obj, f'description_{lang}')

    def get_keywords(self, obj):
        request = self.context.get('request', None)
        lang = request.query_params.get('lang', 'en') if request else 'en'
        return getattr(obj, f'keywords_{lang}')

    def get_article(self, obj):
        request = self.context.get('request', None)
        lang = request.query_params.get('lang', 'en') if request else 'en'
        return getattr(obj, f'article_{lang}')

    def create(self, validated_data):
        tags_data = self.initial_data.get('tags')
        paper = Paper.objects.create(**validated_data)
        if tags_data:
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data)
                paper.tags.add(tag)
        return paper

    def update(self, instance, validated_data):
        tags_data = self.initial_data.get('tags')
        instance = super().update(instance, validated_data)
        if tags_data:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data)
                instance.tags.add(tag)
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'paper', 'content']
