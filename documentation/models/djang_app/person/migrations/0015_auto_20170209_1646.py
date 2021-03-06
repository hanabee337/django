# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0014_auto_20170209_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='following_set', to='person.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='follower_set', to='person.User'),
        ),
    ]
