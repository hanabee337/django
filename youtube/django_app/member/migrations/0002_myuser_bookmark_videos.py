# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20170226_1452'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='bookmark_videos',
            field=models.ManyToManyField(to='video.Video'),
        ),
    ]
