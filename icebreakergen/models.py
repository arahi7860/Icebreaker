from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class IceBreakerQuestionQuerySet(models.QuerySet):
    def filter_by_category_name(self, category_name):
        return self.filter(category__name=category_name)

class IceBreakerQuestionManager(models.Manager):
    def get_queryset(self):
        return IceBreakerQuestionQuerySet(self.model, using=self._db)

    def filter_by_category_name(self, category_name):
        return self.get_queryset().filter_by_category_name(category_name)

class IceBreakerQuestion(models.Model):
    question = models.CharField(max_length=200)
    category = models.ManyToManyField(Category, related_name='questions')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = IceBreakerQuestionManager()

    def __str__(self):
        return self.question
