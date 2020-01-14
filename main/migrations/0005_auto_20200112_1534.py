# Generated by Django 2.2.6 on 2020-01-12 15:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_ventesum'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ventesum',
            options={'ordering': ['room', 'drink', 'quantitySum'], 'verbose_name': 'VenteSum'},
        ),
        migrations.RenameField(
            model_name='ventesum',
            old_name='drinks',
            new_name='drink',
        ),
        migrations.AlterField(
            model_name='ventesum',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]