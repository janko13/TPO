# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-12 12:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps', '0006_auto_20170412_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racunpacient',
            name='casregistracije',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 12, 14, 57, 1, 801232), null=True),
        ),
    ]
