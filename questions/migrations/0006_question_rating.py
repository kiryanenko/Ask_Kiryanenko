# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-18 22:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_merge_20170418_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
