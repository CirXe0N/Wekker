# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20170129_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cast',
            field=models.ManyToManyField(related_name='movie_cast_members', through='api.MovieCastMember', to='api.Person'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='crew',
            field=models.ManyToManyField(related_name='movie_crew_members', through='api.MovieCrewMember', to='api.Person'),
        ),
    ]
