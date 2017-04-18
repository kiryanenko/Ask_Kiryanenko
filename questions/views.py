# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseNotFound, Http404
from questions.models import Question
from django.core.paginator import Paginator, EmptyPage

# Функция пагинации
def paginate(request, objects_list, default_limit=10, pages_count=None):
    try:
        limit = int(request.GET.get('limit', default_limit))
    except ValueError:
        limit = default_limit
    if limit > 100:
        limit = default_limit
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(objects_list, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    if not pages_count:
        page_range = paginator.page_range
    else:
        start = page.number - int(pages_count / 2) - 1
        if start < 0:
            start = 0
        page_range = paginator.page_range[start: page.number + int(pages_count / 2)]
    return page, page_range

# Cписок новых вопросов (главная страница)
def index(request):
    questions = Question.objects.order_by('-created_at')
    page, page_range = paginate(request, questions, default_limit=20, pages_count=7)
    return render(request, 'questions/index.html', {
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    })

def hot(request):
    questions = Question.objects.order_by('-rating')
    page, page_range = paginate(request, questions, default_limit=20, pages_count=7)
    return render(request, 'questions/hot.html', {
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
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
