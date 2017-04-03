from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'questions/index.html', {

    })

def add_question(request):
    return render(request, 'questions/add_question.html', {

    })