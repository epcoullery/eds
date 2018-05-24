from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_Rename_Document_to_Concept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ressource',
            name='type',
            field=models.CharField(choices=[('Savoir', 'savoir'), ('Savoir-faire méthodologique et technique', 'savoir méthodologique'), ('Savoir-faire relationnel', 'savoir relationnel')], default='Savoir', max_length=50),
        ),
    ]
