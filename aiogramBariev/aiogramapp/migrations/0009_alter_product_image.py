# Generated by Django 5.0.6 on 2024-06-07 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiogramapp', '0008_temporary_totalcost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, null=True),
        ),
    ]