from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_extend_ressource_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competence',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.Module'),
        ),
        migrations.AlterField(
            model_name='competence',
            name='proces_eval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.Processus'),
        ),
        migrations.AlterField(
            model_name='competence',
            name='type',
            field=models.CharField(blank=True, max_length=35),
        ),
        migrations.AlterField(
            model_name='domaine',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.Enseignant'),
        ),
        migrations.AlterField(
            model_name='enseignant',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='enseignant',
            name='nom',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='enseignant',
            name='prenom',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='enseignant',
            name='sigle',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='module',
            name='semestre',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='objectif',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cms.Module'),
        ),
        migrations.AlterField(
            model_name='processus',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='ressource',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cms.Module'),
        ),
    ]
