# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-13 17:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps', '0007_auto_20170412_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racunpacient',
            name='casregistracije',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 13, 19, 22, 29, 722062), null=True),
        ),
    ]
