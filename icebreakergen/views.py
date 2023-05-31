from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import IceBreakerQuestion, Category, Profile
from .serializers import IceBreakerQuestionSerializer, CategorySerializer, UserSerializer, ProfileSerializer
from .icebreaker import get_random_question
import json
import random
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken


class CreateIceBreakerQuestionView(viewsets.ModelViewSet):
    queryset = IceBreakerQuestion.objects.all()
    serializer_class = IceBreakerQuestionSerializer

    def create(self, request, *args, **kwargs):
        category_name = request.data.get('category')
        question_text = request.data.get('question')

        if not category_name or not question_text:
            return Response({'message': 'Invalid data format.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the existing data from the JSON file
            with open('questions.json', 'r') as f:
                data = json.load(f)

            categories = data.get('categories', [])

            # Find the category with the specified name
            category = next((c for c in categories if c['name'] == category_name), None)

            if category:
                # Add the question to the category
                category['questions'].append(question_text)

                # Update the JSON file with the modified data
                with open('questions.json', 'w') as f:
                    json.dump(data, f, indent=4)

                # Set a default value for the created_by field
                default_user = User.objects.first()  # Change this to retrieve the actual default user

                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                # Save the instance without committing it to the database
                instance = serializer.save(created_by=default_user)

                # Manually perform any additional operations on the instance if needed

                # Finally, save the instance to the database
                instance.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': f'Category "{category_name}" not found.'}, status=status.HTTP_404_NOT_FOUND)

        except FileNotFoundError:
            return Response({'message': 'Question data file not found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        with open('questions.json', 'r') as f:
            data = json.load(f)
        category_names = [category['name'] for category in data['categories']]
        context['category_names'] = category_names
        return context

    def clear_questions(self, request):
        # Retrieve parameters from the request
        question_text = request.data.get('question_text')
        category_name = request.data.get('category')

        # Find the category instance based on the name
        category_instance = Category.objects.get(name=category_name)

        # Create a filter based on the provided parameters
        filter_params = {}
        if question_text:
            filter_params['question__icontains'] = question_text
        if category_instance:
            filter_params['category'] = category_instance

        # Delete the questions based on the filter
        deleted_count, _ = IceBreakerQuestion.objects.filter(**filter_params).delete()

        return JsonResponse({'message': f'{deleted_count} question(s) deleted successfully.'})

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

        categories = data.get('categories', [])
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
        
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate and set authentication token for the user
        token = generate_auth_token(user)  # Implement your own token generation logic
        user.profile.auth_token = token
        user.profile.save()

        return Response(
            {
                'token': token,
                'username': user.username,
                'email': user.email
            },
            status=status.HTTP_201_CREATED
        )
    
class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'id': user.id, 'username': user.username, 'token': token.key}, status=status.HTTP_200_OK)