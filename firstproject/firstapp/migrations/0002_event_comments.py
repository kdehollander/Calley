# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-05 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='comments',
            field=models.CharField(default='', max_length=140),
            preserve_default=False,
        ),
    ]