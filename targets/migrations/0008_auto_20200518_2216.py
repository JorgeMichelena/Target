# Generated by Django 3.0.3 on 2020-05-18 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0007_auto_20200518_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='picture',
            field=models.ImageField(null='placeholder.png', upload_to='topic-pictures/'),
        ),
    ]
