from rest_framework import serializers
from content.models import Category, Content


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ContentSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'body', 'category', 'category_id', 'metadata',
            'owner', 'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
