# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-13 17:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps', '0009_auto_20170413_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racunpacient',
            name='casregistracije',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 13, 19, 23, 58, 102947), null=True),
        ),
    ]
