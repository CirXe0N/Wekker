# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20170127_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='tv_shows',
            field=models.ManyToManyField(related_name='watchers', to='api.TVShow'),
        ),
    ]
