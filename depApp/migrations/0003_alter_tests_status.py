# Generated by Django 5.0.3 on 2024-03-08 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depApp', '0002_tests_consultation_feedback_message_reports_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tests',
            name='status',
            field=models.CharField(default='Active', max_length=20),
        ),
    ]