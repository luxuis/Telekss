# Generated by Django 2.2.6 on 2019-10-13 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_drinks_is_soldout'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='is_accepter',
            field=models.BooleanField(default=False),
        ),
    ]