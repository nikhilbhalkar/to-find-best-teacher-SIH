# Generated by Django 4.2.5 on 2023-09-22 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_rename_name_ouruser_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ouruser',
            old_name='username',
            new_name='name',
        ),
    ]
