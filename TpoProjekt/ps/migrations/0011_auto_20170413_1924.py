# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-13 17:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps', '0010_auto_20170413_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delavninalog',
            name='casovniIntervalMedDvemaObiskoma',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='delavninalog',
            name='casovnoObdobje',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='delavninalog',
            name='nujnostObiska',
            field=models.CharField(choices=[('obvezen', 'obvezen'), ('okviren', 'okviren')], max_length=50),
        ),
        migrations.AlterField(
            model_name='delavninalog',
            name='podVrstaObiska',
            field=models.CharField(choices=[('obisk nosečnice', 'obisk nosečnice'), ('obisk otročičnice in novorojenčka', 'obisk otročičnice in novorojenčka'), ('preventiva starostnika', 'preventiva starostnika'), ('aplikacija inekcije', 'aplikacija inekcije'), ('odvzem krvi', 'odvzem krvi'), ('kontrola zdravstvenega stanja', 'kontrola zdravstvenega stanja')], max_length=50),
        ),
        migrations.AlterField(
            model_name='delavninalog',
            name='vrstaObiska',
            field=models.CharField(choices=[('preventivni obisk', 'preventivni obisk'), ('kurativni obisk', 'kurativni obisk')], max_length=50),
        ),
        migrations.AlterField(
            model_name='racunpacient',
            name='casregistracije',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 13, 19, 24, 22, 139866), null=True),
        ),
    ]
