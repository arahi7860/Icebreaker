from rest_framework import serializers
from django.contrib.auth.models import User
from .models import IceBreakerQuestion, Category, Profile

class CategorySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, category):
        questions = category['questions']
        return questions

    class Meta:
        model = Category
        fields = ['name', 'questions']

class IceBreakerQuestionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = IceBreakerQuestion
        fields = ('id', 'question', 'categories')

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user