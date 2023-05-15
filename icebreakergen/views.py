from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import IceBreakerQuestion, Category
from .serializers import IceBreakerQuestionSerializer, CategorySerializer
from .icebreaker import get_random_question
import json

class CreateIceBreakerQuestionView(viewsets.ModelViewSet):
    queryset = IceBreakerQuestion.objects.all()
    serializer_class = IceBreakerQuestionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class RandomIceBreakerQuestionView(viewsets.ViewSet):
    queryset = IceBreakerQuestion.objects.all()
    serializer_class = IceBreakerQuestionSerializer

    def retrieve(self, request, pk=None):
        # Get a random question
        question_data = get_random_question()
        category = question_data['category']
        question_text = question_data['question']

        # Create the IceBreakerQuestion object
        category_instance, _ = Category.objects.get_or_create(name=category)
        question_instance = IceBreakerQuestion.objects.create(
            question_text=question_text,
            category=category_instance,
            created_by=request.user
        )

        serializer = self.serializer_class(question_instance)
        return Response(serializer.data)

    def list(self, request):
        # Get a list of all questions
        questions = self.queryset
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data)
    
class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        with open('questions.json', 'r') as f:
            data = json.load(f)

        categories = data['categories']
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        with open('questions.json', 'r') as f:
            data = json.load(f)

        categories = data['categories']
        category = next((c for c in categories if c['name'] == pk), None)
        if category:
            return Response(category)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)