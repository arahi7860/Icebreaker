from rest_framework import serializers
from .models import IceBreakerQuestion, Category

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
