# Generated by Django 2.0.13 on 2022-04-21 19:26

import TSG.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TSG', '0003_auto_20220421_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='UseRights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('own_part', models.DecimalField(decimal_places=2, max_digits=3, validators=[TSG.models.validate_between_one_zero])),
                ('priority', models.IntegerField(default=1)),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TSG.Flat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='flat',
            name='users',
            field=models.ManyToManyField(through='TSG.UseRights', to=settings.AUTH_USER_MODEL),
        ),
    ]
