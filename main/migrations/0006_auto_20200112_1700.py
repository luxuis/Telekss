# Generated by Django 2.2.6 on 2020-01-12 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200112_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ventesum',
            options={'ordering': ['room', 'drink', 'date'], 'verbose_name': 'VenteSum'},
        ),
    ]