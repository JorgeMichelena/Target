# Generated by Django 3.0.3 on 2020-05-19 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200518_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='profile-pictures/240_F_64678017_zUpiZFjj04cnLri7oADnyMH0XBYyQghG.jpg', upload_to='profile-pictures/'),
        ),
    ]
