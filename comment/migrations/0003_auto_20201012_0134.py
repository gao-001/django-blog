# Generated by Django 2.2.16 on 2020-10-11 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20201008_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='website',
        ),
    ]
