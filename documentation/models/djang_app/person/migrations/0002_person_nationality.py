# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='nationality',
            field=models.CharField(default='South Korea', max_length=200),
        ),
    ]
