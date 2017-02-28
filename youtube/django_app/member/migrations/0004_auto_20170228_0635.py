# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 21:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_video_thumbnail_url'),
        ('member', '0003_auto_20170227_0252'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmarkVideos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'member_myuser_bookmark_videos',
            },
        ),
        migrations.AlterField(
            model_name='myuser',
            name='bookmark_videos',
            field=models.ManyToManyField(blank=True, through='member.BookmarkVideos', to='video.Video'),
        ),
        migrations.AddField(
            model_name='bookmarkvideos',
            name='myuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookmarkvideos',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.Video'),
        ),
    ]