# Generated by Django 4.0.3 on 2022-03-13 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_teacher_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='language',
        ),
        migrations.AddField(
            model_name='teacher',
            name='languages',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subjects',
            field=models.TextField(null=True),
        ),
    ]
