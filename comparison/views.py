from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Answer, Economic, UserAnswer
from django.views.decorators.http import require_http_methods


class QuestionListView(ListView):
    model = Question
    template_name = 'comparison/question_list.html'
    context_object_name = 'questions'

class EconomicListView(ListView):
    model = Economic
    template_name = 'comparison/economic_list.html'
    context_object_name = 'economics'

def compare_view(request):
    questions = Question.objects.all()
    economics = Economic.objects.all()
    answers = Answer.objects.all()
    
    # Organize answers by question and economic
    answer_map = {}
    for answer in answers:
        if answer.question.id not in answer_map:
            answer_map[answer.question.id] = {}
        answer_map[answer.question.id][answer.economic.id] = answer.answer
    
    return render(request, 'comparison/compare.html', {
        'layout': layout(request),
        'questions': questions,
        'economics': economics,
        'answer_map': answer_map,
        "cols" : len(economics)+2
    })

def results_view(request):
    results = request.session.get('comparison_results', {})
    if not results:
        return redirect('comparison:compare')
    
    return render(request, 'comparison/results.html', {'results': results})



def poll(request, nr = 0):
    question = Question.objects.all()[nr]
    print(question)
    return render(request, 'comparison/question_.html', {'layout': layout(request), 'question': question, 'nr': nr, 'answer': None})


@require_http_methods(["POST"])
def save_poll(request, nr = 0):
    try:
        question_id = request.POST.get('question_id')
        answer = request.POST.get('answer')
        
        if not question_id or not answer:
            return JsonResponse({'status': 'error', 'message': 'Fehlende erforderliche Felder'}, status=400)
        
        # Create or update UserAnswer
        user_answer, created = UserAnswer.objects.update_or_create(
            question_id=question_id,
            defaults={'answer': answer}
        )
        questions = Question.objects.all()
        if(nr < len(questions)-1):
            next_question = questions[nr+1]
            return render(request, 'comparison/question.html', {'layout': layout(request), 'question': next_question, 'nr': nr+1, 'answer': user_answer})
        else:
            return redirect('comparison:compare')
        
    except Exception as e:
        return JsonResponse({'status': 'error','message': str(e) }, status=500)

def layout(request):
    return "partial.html" if request.htmx else "base.html"
