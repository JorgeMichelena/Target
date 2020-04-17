# Generated by Django 3.0.3 on 2020-03-23 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        ('targets', '0003_target_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='chat.Match'),
            preserve_default=False,
        ),
    ]