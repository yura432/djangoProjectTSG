# Generated by Django 2.0.13 on 2022-04-22 14:54

import TSG.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TSG', '0004_auto_20220421_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userights',
            name='own_part',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, validators=[TSG.models.validate_between_one_zero]),
        ),
    ]
