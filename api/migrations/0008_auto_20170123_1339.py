# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170123_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tvshowcastmember',
            old_name='character_name',
            new_name='character',
        ),
    ]
