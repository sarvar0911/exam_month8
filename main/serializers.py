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

    class Meta:
        model = Publication
        fields = ['id', 'title', 'description', 'file', 'image', 'tags', 'created_at', 'updated_at']


class PaperSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Paper
        fields = '__all__'
        read_only_fields = ['author', 'views', 'date']

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
    paper = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'
