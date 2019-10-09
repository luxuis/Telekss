# Generated by Django 2.2.6 on 2019-10-09 15:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='drinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('container_size', models.IntegerField()),
                ('threshold', models.IntegerField()),
                ('by_bottle', models.IntegerField()),
                ('is_champagne', models.BooleanField()),
            ],
            options={
                'verbose_name': 'drinks',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'food',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drink', models.CharField(max_length=50)),
                ('room', models.CharField(max_length=30)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity', models.IntegerField()),
                ('is_sale', models.BooleanField()),
                ('is_cancelled', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('is_bar', models.BooleanField()),
            ],
            options={
                'verbose_name': 'rooms',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='stocks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('consommation', models.IntegerField()),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.drinks')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.rooms')),
            ],
            options={
                'verbose_name': 'rooms',
                'ordering': ['room', 'drink'],
            },
        ),
        migrations.AddField(
            model_name='rooms',
            name='drinks',
            field=models.ManyToManyField(through='main.stocks', to='main.drinks'),
        ),
    ]