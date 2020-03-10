# Generated by Django 3.0.3 on 2020-03-10 17:28

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import targets.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('picture', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('radius', models.PositiveIntegerField()),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326, validators=[targets.validators.validate_coordinates])),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='targets.Topic')),
            ],
        ),
    ]
