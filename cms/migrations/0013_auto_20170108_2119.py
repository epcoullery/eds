# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 21:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20170104_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competence',
            options={'ordering': ('code',), 'verbose_name': 'compétence'},
        ),
        migrations.AlterModelOptions(
            name='processus',
            options={'ordering': ('code',), 'verbose_name_plural': 'processus'},
        ),
        migrations.AlterModelOptions(
            name='souscompetence',
            options={'ordering': ('code',), 'verbose_name': 'sous-compétence'},
        ),
    ]
