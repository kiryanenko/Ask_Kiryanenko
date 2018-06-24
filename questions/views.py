# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseNotFound, Http404, HttpResponseRedirect
from questions.models import Question, Tag, QuestionLike, AnswerLike, Answer
from questions.forms import SignUpForm, LoginForm, UserSettingsForm, AskForm, AnswerForm
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import re
import math
import json


class HttpResponseAjax(HttpResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(content=json.dumps(kwargs), content_type='application/json')


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(status='error', code=code, message=message)


# Проверка авторизации в AJAX
def login_required_ajax(view):
    def view2(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        elif request.is_ajax():
            return HttpResponseAjaxError(code="no_auth", message=u'Требуется авторизация')
        else:
            HttpResponseRedirect('/login/?continue=' + get_continue(request))
    return view2


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
        start = page.number - pages_count // 2 - 1
        if start < 0:
            start = 0
        page_range = paginator.page_range[start: page.number + int(pages_count / 2)]
    return page, page_range


def get_continue(request, default='/'):
    url = request.GET.get('continue', default)
    if re.match(r'^/|http://127\.0\.0\.', url):   # Защита от Open Redirect
        return url
    return default

# Cписок новых вопросов (главная страница) (URL = /)
def index(request):
    questions = Question.objects.last_questions()
    page, page_range = paginate(request, questions, default_limit=20, pages_count=7)
    return render(request, 'questions/index.html', {
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    })


# Cписок “лучших” вопросов (URL = /hot/)
def hot(request):
    questions = Question.objects.hot_questions()
    page, page_range = paginate(request, questions, default_limit=20, pages_count=7)
    return render(request, 'questions/hot.html', {
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    })


# Cписок вопросов по тэгу (URL = /tag/blablabla/)
def tag(request, tag_name=None):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = tag.question_set.last_questions()
    page, page_range = paginate(request, questions, default_limit=20, pages_count=7)
    return render(request, 'questions/tag.html', {
        'tag': tag,
        'questions': page.object_list,
        'page': page,
        'page_range': page_range,
    })


# Форма создания вопроса (URL = /ask/)
@login_required(login_url='/login', redirect_field_name='continue')
def ask(request):
    if request.method == "POST":
        form = AskForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect('/question/' + str(question.pk))
    else:
        form = AskForm(request.user)
    return render(request, 'questions/ask.html', {
        'form': form,
    })


# Cтраница одного вопроса со списком ответов (URL = /question/35/)
def question(request, question_id=None):
    COUNT_ON_PAGE = 30
    q = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        # Добавление ответа
        form = AnswerForm(request.user, q, request.POST)
        if form.is_valid():
            new_answer = form.save()
            answers = q.answers.hot_answers()
            # Ищу индекс нового ответа
            index = 1
            for ans in answers:
                if ans == new_answer:
                    break
                index += 1
            page = math.ceil(index / COUNT_ON_PAGE)  # страница c новым ответом
            return HttpResponseRedirect('/question/{}?page={}#answer_{}'.format(question_id, page, new_answer.pk))
    else:
        form = AnswerForm(request.user, q)
    answers = q.answers.hot_answers()
    page, page_range = paginate(request, answers, default_limit=COUNT_ON_PAGE, pages_count=7)
    return render(request, 'questions/question.html', {
        'question': q,
        'answers': page.object_list,
        'page': page,
        'page_range': page_range,
        'form': form
    })


# Форма логина (URL = /login/)
def login(request):
    url = get_continue(request)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.auth())
            return HttpResponseRedirect(url)
    else:
        form = LoginForm()
    return render(request, 'questions/login.html', {
        'form': form,
        'continue_url': url,
    })


# Форма регистрации (URL = /signup/)
def signup(request):
    url = get_continue(request)
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login?continue=' + url)
    else:
        form = SignUpForm()
    return render(request, 'questions/signup.html', {
        'form': form,
        'continue_url': url
    })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(get_continue(request))


@login_required(login_url='/login', redirect_field_name='continue')
def settings(request):
    user = request.user
    if request.method == "POST":
        form = UserSettingsForm(user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/settings')
    else:
        form = UserSettingsForm(user, initial={'email': user.email,
                                               'nick_name': user.profile.nick_name,
                                               'avatar': user.profile.avatar})
    return render(request, 'questions/settings.html', {
        'form': form,
    })


# Лайк (дизлайк) вопроса.
# На сервер передаются параметры: id вопроса, тип (лайк / дизлайк). Возвращается: новый рейтинг вопроса или код ошибки.
@login_required_ajax
def question_like(request, question_id=None):
    q = get_object_or_404(Question, id=question_id)
    is_like = request.POST.get('is_like', False)
    rating = QuestionLike.objects.like(request.user, q, is_like)
    if rating is not None:
        return HttpResponseAjax(rating=rating)
    else:
        return HttpResponseAjaxError(code="like_exist", message='Вы уже лайкнули этот вопрос.')


@login_required_ajax
def answer_like(request, answer_id=None):
    q = get_object_or_404(Answer, id=answer_id)
    is_like = request.POST.get('is_like', False)
    rating = AnswerLike.objects.like(request.user, q, is_like)
    if rating is not None:
        return HttpResponseAjax(rating=rating)
    else:
        return HttpResponseAjaxError(code="like_exist", message='Вы уже лайкнули этот ответ.')


@login_required_ajax
def correct_answer(request, question_id=None):
    q = get_object_or_404(Question, id=question_id)
    if request.user != q.user:
        raise HttpResponseBadRequest
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id', 0))
    q.choose_correct_answer(answer)
    return HttpResponseAjax()


def hello_world(request):
    return render(request, 'questions/hello_world.html', {
        'GET': request.GET,
        'POST': request.POST
    })
