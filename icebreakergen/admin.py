from django.contrib import admin
from .models import Category, IceBreakerQuestion

# Register your models here.
admin.site.register(IceBreakerQuestion)
admin.site.register(Category)