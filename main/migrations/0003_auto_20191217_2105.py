# Generated by Django 2.2.6 on 2019-12-17 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_food_is_soldout'),
    ]

    operations = [
        migrations.DeleteModel(
            name='demandeFood',
        ),
        migrations.DeleteModel(
            name='food',
        ),
    ]
