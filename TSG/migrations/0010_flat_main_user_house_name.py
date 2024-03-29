# Generated by Django 4.0.4 on 2022-06-12 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TSG', '0009_announcement_tsg_announcement_users_viewed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='main_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_user_flats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='house',
            name='name',
            field=models.CharField(default='house', max_length=20),
            preserve_default=False,
        ),
    ]
