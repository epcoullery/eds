# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 12:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20161224_0929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competence',
            options={'ordering': ('code',)},
        ),
        migrations.AlterModelOptions(
            name='souscompetence',
            options={'ordering': ('code',)},
        ),
    ]
