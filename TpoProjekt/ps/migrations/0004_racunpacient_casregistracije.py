# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-12 10:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ps', '0003_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='racunpacient',
            name='casregistracije',
            field=models.DateField(default=datetime.datetime(2017, 4, 12, 10, 24, 29, 15763, tzinfo=utc)),
        ),
    ]