# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-06 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0020_auto_20170308_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='texte',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='titre',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]