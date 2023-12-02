# Generated by Django 4.2.5 on 2023-09-22 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_ouruser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='ouruser',
            name='username',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='ouruser',
            name='email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='ouruser',
            name='interest',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='ouruser',
            name='learningstyle',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='ouruser',
            name='level',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='ouruser',
            name='password',
            field=models.CharField(default='', max_length=13),
        ),
    ]
