# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-16 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20170503_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='periode_presentiel',
            field=models.IntegerField(verbose_name='Présentiel'),
        ),
        migrations.AlterField(
            model_name='module',
            name='pratique_prof',
            field=models.IntegerField(default=0, verbose_name='Pratique prof.'),
        ),
    ]