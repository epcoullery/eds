# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-08 10:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0017_document_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='competence',
            name='processus_eval',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Processus'),
        ),
    ]
