from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import IceBreakerQuestion, Category
from .serializers import IceBreakerQuestionSerializer, CategorySerializer
from .icebreaker import get_random_question
import json
import random

class CreateIceBreakerQuestionView(viewsets.ModelViewSet):
    queryset = IceBreakerQuestion.objects.all()
    serializer_class = IceBreakerQuestionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def clear_questions(self, request):
        if request.method == 'POST':
            # Retrieve parameters from the request
            question_text = request.data.get('question_text')
            category = request.data.get('category')

            # Create a filter based on the provided parameters
            filter_params = {}
            if question_text:
                filter_params['question__icontains'] = question_text
            if category:
                filter_params['category__name__iexact'] = category

            # Delete the questions based on the filter
            deleted_count, _ = IceBreakerQuestion.objects.filter(**filter_params).delete()

            return Response({'message': f'{deleted_count} question(s) deleted successfully.'})
        else:
            return Response({'message': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class RandomIceBreakerQuestionView(viewsets.ViewSet):
    serializer_class = IceBreakerQuestionSerializer

    def retrieve(self, request, pk=None):
        question_data = get_random_question()
        category = question_data['category']
        question_text = question_data['question']

        response_data = {
            'question': question_text,
            'category': category  # Include the category name directly
        }
        return Response(response_data)

    def list(self, request):
        questions = []
        count = int(request.query_params.get('count', 5))
        for _ in range(count):
            question_data = get_random_question()
            category = question_data['category']
            question_text = question_data['question']

            questions.append({
                'question': question_text,
                'category': category  # Include the category name directly
            })

        return Response(questions)

    
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