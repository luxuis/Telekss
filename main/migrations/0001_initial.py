# Generated by Django 2.2.7 on 2019-11-30 17:38

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
                ('by_bottle', models.BooleanField()),
                ('is_champagne', models.BooleanField()),
                ('is_soldout', models.BooleanField(default=False)),
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
                ('is_accepter', models.BooleanField(default=False)),
                ('drinks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.drinks')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.rooms')),
            ],
            options={
                'verbose_name': 'stocks',
                'ordering': ['room', 'drinks'],
            },
        ),
        migrations.AddField(
            model_name='rooms',
            name='drinks',
            field=models.ManyToManyField(through='main.stocks', to='main.drinks'),
        ),
        migrations.CreateModel(
            name='history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity', models.IntegerField(default=0)),
                ('is_sale', models.BooleanField()),
                ('is_cancelled', models.BooleanField(default=False)),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.drinks')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.rooms')),
            ],
            options={
                'verbose_name': 'history',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='demandeFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_en_preparation', models.BooleanField(default=False)),
                ('is_en_livraison', models.BooleanField(default=False)),
                ('is_livre', models.BooleanField(default=False)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.food')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.rooms')),
            ],
            options={
                'verbose_name': "demande de degeul'ss",
                'ordering': ['room', 'food'],
            },
        ),
    ]
