# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-02 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beltapp', '0004_auto_20170502_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='destination',
            name='start_date',
            field=models.DateField(),
        ),
    ]
