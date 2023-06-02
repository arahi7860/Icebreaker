"""
URL configuration for icebreaker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from icebreakergen.views import (
    CreateIceBreakerQuestionView,
    RandomIceBreakerQuestionView,
    CategoryViewSet,
    UserCreateView,
    ProfileDetailView,
    ProfileListCreateView,
    CustomAuthToken
)

# Create a router instance
router = routers.DefaultRouter()

# Register your views with the router
router.register('questions/create', CreateIceBreakerQuestionView, basename='question-create')
router.register('questions/random', RandomIceBreakerQuestionView, basename='question-random')
router.register('categories', CategoryViewSet, basename='category')

# Define your URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('questions/create/clear/', CreateIceBreakerQuestionView.as_view({'post': 'clear_questions'}), name='question-clear'),
    path('api/token/', CustomAuthToken.as_view(), name='api-token-auth'),  # Add this line for authentication token endpoint
    path('api/register/', UserCreateView.as_view(), name='api-register'),  # Add this line for user creation endpoint
    path('api/profiles/', ProfileListCreateView.as_view(), name='api-profiles'),  # Optional: Add this line for profiles list and creation endpoint
    path('api/profiles/<int:pk>/', ProfileDetailView.as_view(), name='api-profile-detail'),  # Optional: Add this line for profile detail, update, and delete endpoint
    path('', include(router.urls)),
]
