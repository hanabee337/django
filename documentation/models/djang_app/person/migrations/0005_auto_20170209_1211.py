# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0004_auto_20170209_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nationality',
            field=models.CharField(default='South Korea', max_length=200, verbose_name='국적'),
        ),
        migrations.AlterField(
            model_name='person',
            name='shirt_size',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=1, verbose_name='셔츠 사이즈'),
        ),
    ]
