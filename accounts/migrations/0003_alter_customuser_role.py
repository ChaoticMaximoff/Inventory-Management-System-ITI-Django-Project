# Generated by Django 5.1.7 on 2025-03-11 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('employee', 'Employee'), ('manager', 'Manager')], default='employee', max_length=10),
        ),
    ]
