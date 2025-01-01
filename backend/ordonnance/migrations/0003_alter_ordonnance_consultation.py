# Generated by Django 5.1.4 on 2024-12-27 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0002_alter_consultation_resume'),
        ('ordonnance', '0002_alter_ordonnance_consultation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordonnance',
            name='consultation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ordonnance', to='consultations.consultation'),
        ),
    ]
