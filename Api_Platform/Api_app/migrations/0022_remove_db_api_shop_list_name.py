# Generated by Django 3.2.13 on 2022-10-09 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api_app', '0021_auto_20221009_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_api_shop_list',
            name='name',
        ),
    ]
