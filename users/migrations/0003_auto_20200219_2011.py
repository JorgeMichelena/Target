# Generated by Django 3.0.3 on 2020-02-19 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', 'Not Specified')], default='', max_length=1),
        ),
    ]
