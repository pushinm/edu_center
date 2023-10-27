from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'photo', 'published_at', 'likes_count', 'dislikes_count']


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'video', 'created_at', 'published_at', 'likes_count', 'dislikes_count']


class LikeSerializer(serializers.Serializer):
    token = serializers.CharField()
    news_id = serializers.IntegerField()
