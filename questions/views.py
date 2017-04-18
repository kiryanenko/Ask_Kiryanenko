# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from questions.models import Question
import math

def paginate(objects_list, request, objects_count_per_page):
    page_count = math.ceil(len(objects_list) / objects_count_per_page)
    page = request.GET.get('page') or 1
    try:
        page = int(page)
        if page > page_count:
            raise IndexError
    except ValueError:
        return HttpResponseBadRequest()
    except IndexError:
        return HttpResponseNotFound()
    start_object = (page - 1) * objects_count_per_page
    objects_page = objects_list[start_object:start_object + objects_count_per_page]
    paginator = [p for p in range(page - 2, page + 3) if p > 0 and p <= page_count]
    return objects_page, paginator

# Cписок новых вопросов (главная страница)
def index(request):
    questions = Question.objects.all()
    return render(request, 'questions/index.html', {
        'questions': questions
    })

def hot(request):
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

def login(request):
    return render(request, 'questions/login.html', {

    })

def signup(request):
    return render(request, 'questions/signup.html', {

    })

def hello_world(request):
    return render(request, 'questions/hello_world.html', {
        'GET': request.GET,
        'POST': request.POST
    })
