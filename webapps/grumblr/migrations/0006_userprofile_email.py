# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 02:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20161007_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]