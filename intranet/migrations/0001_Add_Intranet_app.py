from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0009_drop_unneeded_defaults'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntranetDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.FileField(unique=True, upload_to='intranet')),
                ('published', models.BooleanField(default=True)),
                ('authorization', models.SmallIntegerField(choices=[(3, 'admin'), (2, 'prof'), (1, 'étudiant'), (0, 'aucun')], default=0, verbose_name='autorisation')),
                ('module', models.ForeignKey(on_delete=models.deletion.PROTECT, to='cms.Module')),
            ],
            options={
                'verbose_name': 'Document Intranet',
                'verbose_name_plural': 'Documents Intranet',
            },
        ),
    ]
