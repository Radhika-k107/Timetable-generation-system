# Generated by Django 5.1.7 on 2025-03-25 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_alter_subject_code_alter_subject_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='division',
            name='batches',
            field=models.ManyToManyField(blank=True, related_name='divisions', to='timetable.batch'),
        ),
    ]
