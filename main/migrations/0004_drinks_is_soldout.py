# Generated by Django 2.2.6 on 2019-10-13 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191010_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='drinks',
            name='is_soldout',
            field=models.BooleanField(default=False),
        ),
    ]
