# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-27 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_auto_20170108_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competence',
            old_name='libelle',
            new_name='nom',
        ),
        migrations.RenameField(
            model_name='domaine',
            old_name='libelle',
            new_name='nom',
        ),
        migrations.RenameField(
            model_name='processus',
            old_name='libelle',
            new_name='nom',
        ),
        migrations.RenameField(
            model_name='ressource',
            old_name='libelle',
            new_name='nom',
        ),
        migrations.RenameField(
            model_name='souscompetence',
            old_name='libelle',
            new_name='nom',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='processus',
        ),
        migrations.RemoveField(
            model_name='module',
            name='competences',
        ),
        migrations.AddField(
            model_name='competence',
            name='module',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Module'),
        ),
        migrations.AlterField(
            model_name='module',
            name='didactique',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='module',
            name='evaluation',
            field=models.TextField(),
        ),
    ]
