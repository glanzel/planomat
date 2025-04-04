import uuid
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from requests import session
from .models import Question, Answer, Economic, UserAnswer


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
    # Get session UUID
    session_uuid = request.session.get('comparison_uuid')
    if not session_uuid:
        return redirect('comparison:compare')
    
    # Get user answers for this session
    user_answers = UserAnswer.objects.filter(session_uuid=session_uuid)
    if not user_answers.exists():
        return redirect('comparison:compare')
    
    # Get all economics and their answers
    economics = Economic.objects.all()
    results = []
    
    for economic in economics:
        # Get all answers for this economic
        economic_answers = Answer.objects.filter(economic=economic)
        
        # Calculate matches
        match_count = 0
        total_questions = 0
        
        for user_answer in user_answers:
            economic_answer = economic_answers.filter(question=user_answer.question).first()
            if economic_answer and economic_answer.answer == user_answer.answer:
                match_count += 1
            total_questions += 1
        
        # Calculate percentage
        if total_questions > 0:
            percentage = round((match_count / total_questions) * 100, 1)
        else:
            percentage = 0
        
        results.append({
            'economic': economic,
            'percentage': percentage
        })
    
    # Sort results by percentage descending
    results.sort(key=lambda x: x['percentage'], reverse=True)
    
    print(results)
    
    return render(request, 'comparison/results.html', {'layout': layout(request),
        'results': results
    })



def poll(request, nr = 0):
    questions = Question.objects.all()
    if(nr >= len(questions)): return redirect('comparison:results')

    if 'comparison_uuid' not in request.session:
        request.session['comparison_uuid'] = str(uuid.uuid4())
    
    question = questions[nr]
    answer = UserAnswer.objects.filter(question=question, session_uuid=request.session['comparison_uuid']).first()

    return render(request, 'comparison/question_.html', {'layout': layout(request), 'question': question, 'nr': nr, 'answer': answer})

@require_http_methods(["POST"])
def save_poll(request, nr = 0):
    try:
        question_id = request.POST.get('question_id')
        answer = request.POST.get('answer')
        
        if not question_id or not answer:
            return JsonResponse({'status': 'error', 'message': 'Fehlende erforderliche Felder'}, status=400)
        
        # Get or create session UUID
        if 'comparison_uuid' not in request.session:
            request.session['comparison_uuid'] = str(uuid.uuid4())
        
        # Create or update UserAnswer with session UUID
        user_answer, created = UserAnswer.objects.update_or_create(
            question_id=question_id,
            session_uuid=request.session['comparison_uuid'],
            defaults={'answer': answer}
        )
        
        questions = Question.objects.all()
        if(nr < len(questions)-1):
            next_question = questions[nr+1]
            next_answer = UserAnswer.objects.filter(question=next_question, session_uuid=request.session['comparison_uuid']).first()

            return render(request, 'comparison/question.html', {
                'layout': layout(request),
                'question': next_question,
                'nr': nr+1,
                'answer': next_answer
            })
        else:
            return redirect('comparison:results')
        
    except Exception as e:
        return JsonResponse({'status': 'error','message': str(e) }, status=500)

def layout(request):
    return "partial.html" if request.htmx else "base.html"
