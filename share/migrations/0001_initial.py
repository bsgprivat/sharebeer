# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 10:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('Thumbnail', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('Image', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('bulk_only', models.BooleanField(default=False, help_text='Only sold in multipacks')),
                ('bulk_size', models.IntegerField(blank=True, default=False, help_text='Multipack limit', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BeerSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.DecimalField(decimal_places=1, help_text='Volume in centiliters', max_digits=5)),
                ('container', models.IntegerField(choices=[(0, 'Can'), (1, 'Bottle, glass'), (2, 'Bottle, plastic')])),
                ('approx_weight', models.IntegerField(blank=True, help_text='weight in grams', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('Logotype, thumbnail', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('Logotype, Large', models.ImageField(blank=True, null=True, upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='ShareUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingCosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('free_shipping_limit', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('Logotype', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('currency', models.CharField(max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='shippingcosts',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.Site'),
        ),
        migrations.AddField(
            model_name='beer',
            name='breweries',
            field=models.ManyToManyField(to='share.Brewery'),
        ),
        migrations.AddField(
            model_name='beer',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.BeerSize'),
        ),
    ]
