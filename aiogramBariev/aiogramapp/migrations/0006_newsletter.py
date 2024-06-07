# Generated by Django 5.0.6 on 2024-06-06 21:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiogramapp', '0005_remove_basket_tg_user_basket_tg_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('tg_user_list', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(max_length=20), size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]