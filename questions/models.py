# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager

# Create your models here.
class Profile(User):
    avatar = models.ImageField(upload_to='avatars', default='avatars/user.png')
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(Profile)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
