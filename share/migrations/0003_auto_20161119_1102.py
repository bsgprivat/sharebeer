# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0002_auto_20161119_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beer',
            name='breweries',
        ),
        migrations.AddField(
            model_name='beer',
            name='brewery',
            field=models.ManyToManyField(related_name='beers', to='share.Brewery'),
        ),
        migrations.AddField(
            model_name='beer',
            name='collabs',
            field=models.ManyToManyField(related_name='collab_beers', to='share.Brewery'),
        ),
        migrations.AlterField(
            model_name='beer',
            name='bulk_size',
            field=models.IntegerField(blank=True, help_text='Multipack limit', null=True),
        ),
    ]
