# Generated by Django 5.1.7 on 2025-03-11 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='full_name',
        ),
    ]
