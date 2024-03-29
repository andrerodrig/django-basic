'''
Criar as funções que vão representar as páginas 
Fazer conexção com o Banco de dados renderizando as classes
importadas nas páginas através dos templates.
'''


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

#from django.template import loader

from .models import Choice, Question

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request,'polls/index.html',context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html',{'question': question})

def results(request, question_id):
    response = "You're at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message': 'Your didn\'t select a choice.',
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with OPST data. This prevents data from being posted twice if a
        # user hist the Back button

        return HttpResponseRedirect(reverse('polls:results', args=(question.id)))