# Generated by Django 3.2.13 on 2022-07-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_app', '0010_db_notice_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_power',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('users', models.CharField(blank=True, default='[]', max_length=500, null=True)),
            ],
        ),
    ]
