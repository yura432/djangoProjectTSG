# Generated by Django 2.0.13 on 2022-04-28 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='recipients',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='tsg',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
