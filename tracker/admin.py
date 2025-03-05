from django.contrib import admin

# Register your models here.

from .models import Journal, Question, Choice
admin.site.register(Journal)
admin.site.register(Question)
admin.site.register(Choice)