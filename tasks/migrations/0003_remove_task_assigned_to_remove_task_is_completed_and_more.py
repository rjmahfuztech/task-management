# Generated by Django 5.1.4 on 2025-02-02 05:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_taskdetails_assigned_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='task',
            name='is_completed',
        ),
        migrations.AlterField(
            model_name='taskdetails',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='taskdetails',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='details', to='tasks.task'),
        ),
    ]
