# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20170130_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvshowepisode',
            name='air_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
