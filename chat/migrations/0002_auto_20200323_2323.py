# Generated by Django 3.0.3 on 2020-03-23 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0005_remove_target_match'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='target1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches1', to='targets.Target'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='target2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches2', to='targets.Target'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatlog', to='chat.Match'),
        ),
    ]
