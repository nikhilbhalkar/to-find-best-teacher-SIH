# Generated by Django 4.2.5 on 2023-09-22 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_ouruser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ouruser',
            name='user',
        ),
    ]