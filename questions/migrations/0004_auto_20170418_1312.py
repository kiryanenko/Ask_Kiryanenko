# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-18 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20170417_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatars/user.png', upload_to='avatars'),
        ),
    ]