# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 05:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_postmanager_postuservisiblemanager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
    ]
