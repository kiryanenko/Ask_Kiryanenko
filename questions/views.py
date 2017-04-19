# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseNotFound, Http404
from questions.models import Profile, Question, Tag
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

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

# Cписок новых вопросов (главная страница) (URL = /)
def index(request):
    questions = Question.objects.order_by('-created_at')
    page, page_range = paginate(request, questions, default_limit=20, pages_count=7)
    return render(request, 'questions/index.html', {
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    })

# Cписок “лучших” вопросов (URL = /hot/)
def hot(request):
    questions = Question.objects.order_by('-rating')
    page, page_range = paginate(request, questions, default_limit=20, pages_count=7)
    return render(request, 'questions/hot.html', {
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    })

# Cписок вопросов по тэгу (URL = /tag/blablabla/)
def tag(request, tag_name=None):
    try:
        tag = Tag.objects.get(name=tag_name)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest()
    questions = tag.question_set.order_by('-created_at')
    page, page_range = paginate(request, questions, default_limit=20, pages_count=7)
    return render(request, 'questions/tag.html', {
        'tag': tag,
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    })

def ask(request):
    return render(request, 'questions/ask.html', {

    })

# Cтраница одного вопроса со списком ответов (URL = /question/35/)
def question(request, question_id=None):
    try:
        q = Question.objects.get(id=question_id)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest()
    answers = q.answers.order_by('-created_at')
    page, page_range = paginate(request, answers, default_limit=30, pages_count=7)
    return render(request, 'questions/question.html', {
        'question': q,
        'answers': page.object_list,
        'page': page,
        'page_range': page_range,
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
