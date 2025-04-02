from django.contrib import admin
from .models import Question, Answer, Economic

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at', 'updated_at')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'economic', 'answer', 'created_at', 'updated_at')
    list_filter = ('answer',)

@admin.register(Economic)
class EconomicAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
