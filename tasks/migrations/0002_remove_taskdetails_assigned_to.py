# Generated by Django 5.1.4 on 2025-01-22 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskdetails',
            name='assigned_to',
        ),
    ]
