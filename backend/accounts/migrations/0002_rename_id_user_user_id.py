# Generated by Django 5.1.4 on 2024-12-17 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='id_user',
            new_name='id',
        ),
    ]
