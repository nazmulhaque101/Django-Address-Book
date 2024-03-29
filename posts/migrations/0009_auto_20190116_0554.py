# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-15 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_remove_post_publish'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['fullname']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
        migrations.RemoveField(
            model_name='post',
            name='draft',
        ),
        migrations.RemoveField(
            model_name='post',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated',
        ),
        migrations.AddField(
            model_name='post',
            name='address',
            field=models.TextField(default='N/A'),
        ),
        migrations.AddField(
            model_name='post',
            name='email',
            field=models.CharField(default='N/A', max_length=120),
        ),
        migrations.AddField(
            model_name='post',
            name='fullname',
            field=models.CharField(default='N/A', max_length=120),
        ),
        migrations.AddField(
            model_name='post',
            name='nickname',
            field=models.CharField(default='N/A', max_length=120),
        ),
        migrations.AddField(
            model_name='post',
            name='phone',
            field=models.CharField(default='N/A', max_length=20),
        ),
    ]
