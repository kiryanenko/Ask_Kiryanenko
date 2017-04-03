from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'questions/index.html', {

    })

def ask(request):
    return render(request, 'questions/ask.html', {

    })