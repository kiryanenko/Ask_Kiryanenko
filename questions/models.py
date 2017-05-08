# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager


class Profile(User):
    nick_name = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatars', default='avatars/user.png')
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def last_questions(self):
        return self.order_by('-created_at')

    def hot_questions(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(Profile)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    correct_answer = models.OneToOneField('Answer', related_name='+', null=True, blank=True)
    objects = QuestionManager()

    def __str__(self):
        return '{}; user: {}; updated_at: {}'.format(self.title, self.user, self.updated_at)


class AnswerManager(models.Manager):
    def last_answers(self):
        return self.order_by('-created_at')


class Answer(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')
    user = models.ForeignKey(Profile)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AnswerManager()

    def __str__(self):
        return '{}; updated_at: {}; {}'.format(self.user, self.updated_at, self.text)


class QuestionLike(models.Model):
    user = models.ForeignKey(Profile)
    question = models.ForeignKey(Question)
    is_like = models.BooleanField()

class AnswerLike(models.Model):
    user = models.ForeignKey(Profile)
    answer = models.ForeignKey(Answer)
    is_like = models.BooleanField()
