from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'questions/index.html', {

    })

def ask(request):
    return render(request, 'questions/ask.html', {

    })

def question(request):
    q = {
        'title': 'Заголовок вопроса?',
        'text': 'Some quick example text to build on the card title and make up the bulk of the card. Example. ' * 3,
        'rating': 123
    }
    tags = ['Some', 'quick', 'example']
    answers = [{
        'text': 'Some quick example text to build on the card title and make up the bulk of the card. Example. ' * 3,
        'rating': 123
    }, ] * 15

    return render(request, 'questions/question.html', {
        'question': q,
        'tags': tags,
        'answers': answers,
    })

