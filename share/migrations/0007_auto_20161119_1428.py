# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0006_auto_20161119_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='abv',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
        migrations.AlterField(
            model_name='currency',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=2, help_text='Exchange rate against SEK, ie: if 1DKK = 1.30SEK, supplied value should be 1.3', max_digits=5),
        ),
    ]
