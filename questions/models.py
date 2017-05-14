# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars', default='avatars/user.png')

# определим сигналы, чтобы наша модель Profile автоматически обновлялась при создании/изменении данных модели User.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def last_questions(self):
        return self.order_by('-created_at')

    def hot_questions(self):
        return self.order_by('-rating', '-created_at')


class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    correct_answer = models.OneToOneField('Answer', related_name='+', null=True, blank=True)
    objects = QuestionManager()

    def update_rating(self):
        self.rating = 0
        for like in self.questionlike_set.all():
            self.rating += 1 if like.is_like else -1
        self.save()
        return self.rating

    def liked_users(self):
        return User.objects.filter(questionlike__question=self, questionlike__is_like=True)

    def disliked_users(self):
        return User.objects.filter(questionlike__question=self, questionlike__is_like=False)

    def choose_correct_answer(self, answer):
        if answer in self.answers:
            self.correct_answer = answer
            self.save()

    def __str__(self):
        return '{}; user: {}; updated_at: {}'.format(self.title, self.user, self.updated_at)


class AnswerManager(models.Manager):
    def hot_answers(self):
        return self.order_by('-rating', '-created_at')


class Answer(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AnswerManager()

    def update_rating(self):
        self.rating = 0
        for like in self.answerlike_set.all():
            self.rating += 1 if like.is_like else -1
        self.save()
        return self.rating

    def liked_users(self):
        return User.objects.filter(answerlike__answer=self, answerlike__is_like=True)

    def disliked_users(self):
        return User.objects.filter(answerlike__answer=self, answerlike__is_like=False)

    def __str__(self):
        return '{}; updated_at: {}; {}'.format(self.user, self.updated_at, self.text)


class QuestionLikeManager(models.Manager):
    def like(self, user, question, is_like):
        like, is_create = self.get_or_create(user=user, question=question)
        like.is_like = is_like
        like.save()
        return question.update_rating()


class QuestionLike(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    is_like = models.BooleanField(default=True)
    objects = QuestionLikeManager()


class AnswerLikeManager(models.Manager):
    def like(self, user, answer, is_like):
        like, is_create = self.get_or_create(user=user, answer=answer)
        like.is_like = is_like
        like.save()
        return answer.update_rating()


class AnswerLike(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    is_like = models.BooleanField(default=True)
    objects = AnswerLikeManager()
