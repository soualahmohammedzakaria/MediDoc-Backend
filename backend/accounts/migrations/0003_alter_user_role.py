# Generated by Django 5.1.4 on 2024-12-21 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_id_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('patient', 'Patient'), ('medecin', 'Médecin'), ('radiologue', 'Radiologue'), ('laborantin', 'Laborantin'), ('infirmier', 'Infirmier'), ('administratif', 'Administratif')], max_length=15),
        ),
    ]
