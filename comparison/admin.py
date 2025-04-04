from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import Question, Answer, Economic

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'description']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'answers_link', 'created_at', 'updated_at' )
    search_fields = ('text', 'description')

    def answers_link(self, obj):
        url = reverse('admin:question_answers', args=[obj.id])
        return format_html('<a href="{}">Edit Answers</a>', url)
    answers_link.short_description = 'Answers'  # Spaltenname in der Liste

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:question_id>/answers/',self.admin_site.admin_view(self.edit_answers),name='question_answers',),
        ]
        return custom_urls + urls
    
    def edit_answers(self, request, question_id):
        economics = Economic.objects.all()
        print(economics)
        question = Question.objects.get(pk=question_id)
        AnswerFormSet = forms.formset_factory(AnswerForm, extra=0)

        if request.method == 'POST':
            formset = AnswerFormSet(request.POST)
            if formset.is_valid():
                for i, form in enumerate(formset):
                    economic = economics[i]
                    answer_text = form.cleaned_data.get('answer', '')
                    Answer.objects.update_or_create(
                        question=question,
                        economic=economic,
                        defaults={'answer': answer_text}
                    )
                return HttpResponseRedirect(
                    reverse('admin:comparison_economic_changelist')
                )
        else:
            initial_data = []
            for economic in economics:
                answer = Answer.objects.filter(
                    question=question,
                    economic=economic
                ).first()
                initial_data.append({
                    'answer': answer.answer if answer else ''
                })
            formset = AnswerFormSet(initial=initial_data)

        context = {
            'formset': formset,
            'question': question,
            'economics': zip(economics, formset),
            'opts': self.model._meta,
            'title': f"Edit Answers for {question.text}",
            'is_nav_sidebar_enabled': True, 
            **self.admin_site.each_context(request), 
        }
        return render(
            request,
            'admin/answers_question_form.html',
            context
        )


@admin.register(Economic)
class EconomicAdmin(admin.ModelAdmin):
    list_display = ('name', 'answers_link', 'created_at', 'updated_at' )
    search_fields = ('name', 'description')

    def answers_link(self, obj):
        url = reverse('admin:economic_answers', args=[obj.id])
        return format_html('<a href="{}">Edit Answers</a>', url)
    answers_link.short_description = 'Answers'  # Spaltenname in der Liste

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:economic_id>/answers/',self.admin_site.admin_view(self.edit_answers),name='economic_answers',),
        ]
        return custom_urls + urls

    def edit_answers(self, request, economic_id):
        economic = Economic.objects.get(pk=economic_id)
        questions = Question.objects.all()
        AnswerFormSet = forms.formset_factory(AnswerForm, extra=0)

        if request.method == 'POST':
            formset = AnswerFormSet(request.POST)
            if formset.is_valid():
                for i, form in enumerate(formset):
                    question = questions[i]
                    answer_text = form.cleaned_data.get('answer', '')
                    Answer.objects.update_or_create(
                        question=question,
                        economic=economic,
                        defaults={'answer': answer_text}
                    )
                return HttpResponseRedirect(
                    reverse('admin:comparison_economic_changelist')
                )
        else:
            initial_data = []
            for question in questions:
                answer = Answer.objects.filter(
                    question=question,
                    economic=economic
                ).first()
                initial_data.append({
                    'answer': answer.answer if answer else ''
                })
            formset = AnswerFormSet(initial=initial_data)

        context = {
            'formset': formset,
            'economic': economic,
            'questions': zip(questions, formset),
            'opts': self.model._meta,
            'title': f"Edit Answers for {economic.name}",
            'is_nav_sidebar_enabled': True, 
            **self.admin_site.each_context(request), 
        }
        return render(
            request,
            'admin/answers_form.html',
            context
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['answers_url'] = reverse(
            'admin:economic_answers',
            args=[object_id]
        )
        return super().change_view(request, object_id, form_url, extra_context)