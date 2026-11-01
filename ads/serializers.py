from rest_framework import serializers
from .models import Ad, Review
from users.serializers import UserSerializer

class AdSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'title', 'price', 'description', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'ad', 'created_at']
        read_only_fields = ['author', 'created_at']